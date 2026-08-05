                        performance_logs = driver.get_log("performance")
                        self._classify_browser_logs(result, browser_logs, performance_logs, server.origin)
                        interaction = driver.execute_script(SAFE_INTERACTION_JS) or {}
                        target = interaction.pop("element", None) if isinstance(interaction, dict) else None
                        if target is not None:
                            try:
                                target.click()
                                interaction["clicked"] = True
                            except Exception as exc:
                                interaction["clicked"] = False
                                interaction["reason"] = f"{type(exc).__name__}: {exc}"
                        if interaction and interaction.get("clicked"):
                            time.sleep(min(settle, 0.35))
                            interaction["post_errors"] = driver.execute_script("return window.__estateAuditErrors || []") or []
                            post_logs = driver.get_log("browser")
                            post_perf = driver.get_log("performance")
                            self._classify_browser_logs(result, post_logs, post_perf, server.origin)
                        result["interaction"] = interaction
                        if not surface or not surface.get("has_surface"):
                            result["errors"].append({"kind": "render", "message": "Page completed without visible text or renderable media"})
                        if surface and surface.get("unnamed_controls", 0):
                            result["warnings"].append({"kind": "a11y", "message": f"{surface['unnamed_controls']} visible controls have no accessible name"})
                        result["status"] = "fail" if result["errors"] or result["local_http_errors"] else "pass"
                    except TimeoutException as exc:
                        result["status"] = "fail"
                        result["errors"].append({"kind": "timeout", "message": str(exc)[:2000]})
                        with contextlib.suppress(Exception):
                            driver.execute_script("window.stop()")
                    except WebDriverException as exc:
                        result["status"] = "fail"
                        result["errors"].append({"kind": "webdriver", "message": str(exc)[:2000]})
                    except Exception as exc:
                        result["status"] = "fail"
                        result["errors"].append({"kind": "audit", "message": f"{type(exc).__name__}: {exc}"})
                    self.browser_results.append(result)
                    if result["status"] == "fail":
                        severity = "error" if public else "warning"
                        details = json.dumps({"mode": mode, "errors": result["errors"][:8], "http": result["local_http_errors"][:8]}, ensure_ascii=False)
                        self.add(severity, "browser", rel, f"Browser smoke failed in {mode}", details=details, blocking=public)
                    with contextlib.suppress(Exception):
                        driver.execute_script("try{localStorage.clear();sessionStorage.clear();}catch(e){}")
                # Keep a progress marker in Actions logs without flooding one line per page.
                print(f"browser mode {mode}: probed {len(html_paths)} HTML files", flush=True)
        except Exception as exc:
            self.add("error", "browser", "<estate>", "Browser session could not start or complete", details=f"{type(exc).__name__}: {exc}\n{traceback.format_exc()[-4000:]}")
        finally:
            if driver is not None:
                with contextlib.suppress(Exception):
                    driver.quit()
            server.stop()
        counts = Counter(result.get("status", "unknown") for result in self.browser_results)
        self.metrics["browser"] = {
            "modes": list(modes),
            "result_count": len(self.browser_results),
            "status_counts": dict(counts),
        }

    @staticmethod
    def _configure_browser_mode(driver: Any, mode: str) -> None:
        reduced = "reduced" in mode
        mobile = "mobile" in mode
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {
            "media": "screen",
            "features": [{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}],
        })
        if mobile:
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 390,
                "height": 844,
                "deviceScaleFactor": 3,
                "mobile": True,
                "screenWidth": 390,
                "screenHeight": 844,
            })
            driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {
                "enabled": True,
                "maxTouchPoints": 5,
            })
            driver.set_window_size(390, 844)
        else:
            with contextlib.suppress(Exception):
                driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})
            driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {
                "enabled": False,
                "maxTouchPoints": 0,
            })
            driver.set_window_size(1440, 1000)

    @staticmethod
    def _classify_browser_logs(result: dict[str, Any], browser_logs: Sequence[dict[str, Any]], performance_logs: Sequence[dict[str, Any]], origin: str) -> None:
        for entry in browser_logs:
            level = str(entry.get("level", "")).upper()
            message = str(entry.get("message", ""))
            if level != "SEVERE":
                continue
            lower = message.lower()
            if "favicon.ico" in lower or "manifest.json" in lower:
                continue
            if "failed to load resource" in lower:
                # Exact local HTTP failures are derived from Network.responseReceived below.
                continue
            result["errors"].append({"kind": "console", "message": message[:2000]})
        parsed_logs: list[dict[str, Any]] = []
        request_methods: dict[str, str] = {}
        for entry in performance_logs:
            try:
                payload = json.loads(entry["message"])["message"]
                parsed_logs.append(payload)
                if payload.get("method") == "Network.requestWillBeSent":
                    params = payload.get("params", {})
                    request_id = str(params.get("requestId", ""))
                    request = params.get("request", {})
                    if request_id:
                        request_methods[request_id] = str(request.get("method", "GET")).upper()
            except Exception:
                continue
        for payload in parsed_logs:
            try:
                if payload.get("method") != "Network.responseReceived":
                    continue
                params = payload.get("params", {})
                response = params["response"]
                status = int(response.get("status", 0))
                url = str(response.get("url", ""))
                if status < 400 or not url.startswith(origin):
                    continue
                if url.endswith("/favicon.ico"):
                    continue
                request_id = str(params.get("requestId", ""))
                method = request_methods.get(request_id, "GET")
                path = urllib.parse.urlsplit(url).path.rstrip("/")
                optional_static_probe = path.endswith("/sync.php") or path.endswith("/sync")
                record = {"status": status, "url": url, "method": method}
                if optional_static_probe:
                    result.setdefault("optional_http_failures", []).append(record)
                    result["warnings"].append({
                        "kind": "optional-http",
                        "message": f"Optional classroom endpoint returned HTTP {status}: {method} {url}",
                    })
                else:
                    result["local_http_errors"].append(record)
            except Exception:
                continue

    def _live_probe(self) -> None:
        # Verify high-value files exactly before the broader HTTP census.
        exact_checks = [
            ("https://madebymatt.uk/Lessons/index.html", "lessons", "index.html", "Lessons index.html"),
            ("https://madebymatt.uk/Lessons/resources.json", "lessons", "resources.json", "Lessons resources.json"),
            ("https://madebymatt.uk/site.json", "site", "site.json", "website site.json"),
        ]
        for url, universe, rel, label in exact_checks:
            result = self._fetch_url(url, full=True)
            result["label"] = label
            result["source_ref"] = self.published_ref if universe == "lessons" else "site checkout main"
            local = self._published_bytes(rel) if universe == "lessons" else self._read_optional(self.site_root / rel)
            if result.get("ok") and local is not None:
                remote = result.pop("body", b"")
                result["local_sha256"] = hashlib.sha256(local).hexdigest()
                result["live_sha256"] = hashlib.sha256(remote).hexdigest()
                result["exact_match"] = local == remote
                if not result["exact_match"]:
                    self.add("error", "live", label, "Live file does not byte-match repository main", details=url)
            elif local is None:
                self.add("error", "live", label, "Published source file could not be read", details=f"{universe}:{rel}")
            elif not result.get("ok"):
                self.add("error", "live", label, "High-value live file could not be fetched", details=json.dumps(self._json_safe(result)))
            self.live_results.append(self._json_safe(result))
        paths: set[str] = {"index.html", "resources.json"}
        for rel, record in self.html.items():
            if record.public:
                paths.add(rel)
        for target in self.resolved_public_targets:
            if self._is_public_path(target):
                paths.add(target)
        # Keep the census bounded and deterministic; a truncation is itself visible evidence.
        ordered = sorted(paths)
        cap = 3000
        if len(ordered) > cap:
            self.add("warning", "live", "<estate>", f"Live census capped at {cap} of {len(ordered)} public paths", blocking=False)
            ordered = ordered[:cap]
        urls = [(rel, "https://madebymatt.uk/Lessons/" + urllib.parse.quote(rel, safe="/")) for rel in ordered]
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
            futures = {pool.submit(self._fetch_url, url, False): (rel, url) for rel, url in urls}
            for future in concurrent.futures.as_completed(futures):
                rel, url = futures[future]
                try:
                    result = future.result()
                except Exception as exc:
                    result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
                result.update({"path": rel, "url": url, "kind": "public-path"})
                self.live_results.append(self._json_safe(result))
                if not result.get("ok"):
                    self.add("error", "live", rel, "Public path is not live", details=json.dumps(self._json_safe(result)), blocking=True)
        self._pages_api_check("MattRoper1977/Lessons")
        self._pages_api_check("MattRoper1977/mattroper1977.github.io")
        live_counts = Counter("pass" if result.get("ok") else "fail" for result in self.live_results if result.get("kind") == "public-path")
        self.metrics["live"] = {
            "public_path_count": sum(live_counts.values()),
            "status_counts": dict(live_counts),
            "exact_checks": [result for result in self.live_results if result.get("label")],
        }

    def _published_bytes(self, rel: str) -> bytes | None:
        proc = subprocess.run(
            ["git", "show", f"{self.published_ref}:{rel}"],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode == 0:
            return proc.stdout
        # Local manual runs may not have an origin/main ref yet. Falling back to
        # the working tree is visible in the evidence and never silent.
        fallback = self._read_optional(self.root / rel)
        self.add(
            "warning", "live", rel,
            f"Could not read {self.published_ref}; live comparison used the working tree",
            details=proc.stderr.decode("utf-8", "replace").strip(), blocking=False,
        )
        return fallback

    @staticmethod
    def _read_optional(path: pathlib.Path) -> bytes | None:
        try:
            return path.read_bytes()
        except OSError:
            return None

    def _pages_api_check(self, repo: str) -> None:
        token = os.environ.get("GITHUB_TOKEN", "")
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "lessons-estate-audit"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            headers["X-GitHub-Api-Version"] = "2022-11-28"
        for suffix, label in (("pages", "pages-config"), ("pages/builds/latest", "pages-latest-build")):
            url = f"https://api.github.com/repos/{repo}/{suffix}"
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    body = json.loads(response.read().decode("utf-8"))
                record = {"kind": label, "repo": repo, "ok": True, "status": response.status, "data": body}
                self.live_results.append(record)
                if label == "pages-config" and repo.endswith("/Lessons"):
                    source = body.get("source") or {}
                    branch = source.get("branch")
                    if branch and branch != "main":
                        self.add("error", "live", repo, f"GitHub Pages source branch is {branch}, not main")
                if label == "pages-latest-build":
                    status = str(body.get("status", "")).lower()
                    if status and status not in {"built", "success"}:
                        self.add("error", "live", repo, f"Latest Pages build status is {status}")
            except urllib.error.HTTPError as exc:
                # The endpoint can be permission-gated even when the public site is healthy.
                self.live_results.append({"kind": label, "repo": repo, "ok": False, "status": exc.code, "error": str(exc)})
                self.add("warning", "live", repo, f"Could not read {label} API evidence (HTTP {exc.code})", blocking=False)
            except Exception as exc:
                self.live_results.append({"kind": label, "repo": repo, "ok": False, "error": str(exc)})
                self.add("warning", "live", repo, f"Could not read {label} API evidence", details=str(exc), blocking=False)

    @staticmethod
    def _fetch_url(url: str, full: bool = False) -> dict[str, Any]:
        headers = {"User-Agent": "LessonsEstateAudit/1.0", "Accept": "*/*"}
        method = "GET" if full else "HEAD"
        req = urllib.request.Request(url, method=method, headers=headers)
        started = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                body = response.read() if full else b""
                return {
                    "ok": 200 <= response.status < 400,
                    "status": response.status,
                    "final_url": response.geturl(),
                    "content_type": response.headers.get("Content-Type", ""),
                    "content_length": response.headers.get("Content-Length"),
                    "elapsed_ms": round((time.monotonic() - started) * 1000),
                    "body": body,
                }
        except urllib.error.HTTPError as exc:
