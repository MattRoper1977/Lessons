                return attrs[key].strip()
        text = " ".join(part.strip() for part in element.itertext() if part.strip())
        if text:
            return text
        if attrs.get("aria-labelledby"):
            return attrs["aria-labelledby"]
        if tag == "select":
            return "select-options" if list(element) else ""
        return ""

    @staticmethod
    def _parse_attrs(raw: str) -> dict[str, str]:
        attrs: dict[str, str] = {}
        pattern = re.compile(r"([^\s=/>]+)(?:\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+)))?")
        for match in pattern.finditer(raw):
            key = match.group(1).lower()
            value = next((group for group in match.groups()[1:] if group is not None), "")
            attrs[key] = html_module.unescape(value)
        return attrs

    @staticmethod
    def _parse_srcset(srcset: str) -> list[str]:
        results: list[str] = []
        for chunk in srcset.split(","):
            candidate = chunk.strip().split()[0] if chunk.strip() else ""
            if candidate:
                results.append(candidate)
        return results

    @staticmethod
    def _find_attribute_line(text: str, value: str | None) -> int | None:
        if not value:
            return None
        index = text.find(value)
        return text.count("\n", 0, index) + 1 if index >= 0 else None

    def _module_script_targets(self) -> set[str]:
        targets: set[str] = set()
        script_pattern = re.compile(r"<script\b(?P<attrs>[^>]*)>", re.I | re.S)
        for source, source_text in self._text_cache.items():
            if pathlib.PurePosixPath(source).suffix.lower() not in {".html", ".htm"}:
                continue
            public = self._is_public_path(source)
            for match in script_pattern.finditer(source_text):
                attrs = self._parse_attrs(match.group("attrs"))
                if attrs.get("type", "").strip().lower() != "module":
                    continue
                src = attrs.get("src", "").strip()
                if not src:
                    continue
                line = source_text.count("\n", 0, match.start()) + 1
                resolved = self._resolve_reference(RefRecord(source, "src", src, line, public))
                if resolved and resolved[0] == "lessons":
                    targets.add(resolved[1])
        return targets

    def _validate_resources_schema(self) -> None:
        resources_path = self.root / "resources.json"
        schema_path = self.root / "resources.schema.json"
        if not resources_path.exists():
            self.add("error", "catalog", "resources.json", "Resource catalog is missing")
            return
        if not schema_path.exists():
            self.add("error", "catalog", "resources.schema.json", "Resource catalog schema is missing")
            return
        try:
            resources = json.loads(resources_path.read_text(encoding="utf-8"))
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.add("error", "catalog", "resources.json", "Catalog/schema could not be loaded", details=str(exc))
            return
        if jsonschema is not None:
            try:
                validator_cls = jsonschema.validators.validator_for(schema)
                validator_cls.check_schema(schema)
                validator = validator_cls(schema)
                errors = sorted(validator.iter_errors(resources), key=lambda err: list(err.absolute_path))
                for error in errors:
                    path = "/".join(str(part) for part in error.absolute_path) or "<root>"
                    self.add("error", "catalog", "resources.json", f"Schema validation failed at {path}", details=error.message)
            except Exception as exc:
                self.add("error", "catalog", "resources.schema.json", "Schema validator failed", details=str(exc))
        keys: list[str] = []
        for item in self._walk_objects(resources):
            for key_name in ("id", "key", "slug"):
                value = item.get(key_name)
                if isinstance(value, str) and value.strip():
                    keys.append(f"{key_name}:{value.strip()}")
        duplicates = [key for key, count in Counter(keys).items() if count > 1]
        for duplicate in sorted(duplicates):
            self.add("warning", "catalog", "resources.json", f"Duplicate catalog identifier: {duplicate}", blocking=False)
        self.metrics["catalog_object_count"] = sum(1 for _ in self._walk_objects(resources))

    @staticmethod
    def _walk_objects(value: Any) -> Iterator[dict[str, Any]]:
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from Audit._walk_objects(child)
        elif isinstance(value, list):
            for child in value:
                yield from Audit._walk_objects(child)

    def _resolve_all_references(self) -> None:
        seen: set[tuple[str, str, str]] = set()
        for record in self.references:
            key = (record.source, record.attribute, record.value)
            if key in seen:
                continue
            seen.add(key)
            value = record.value.strip()
            if not value or value.startswith("#"):
                if value.startswith("#") and len(value) > 1:
                    fragment = urllib.parse.unquote(value[1:])
                    source_record = self.html.get(record.source)
                    if source_record and fragment not in source_record.ids:
                        self.add("warning", "reference", record.source, f"Fragment target is missing: {value}", line=record.line, blocking=False)
                continue
            resolved = self._resolve_reference(record)
            if not resolved:
                continue
            universe, target, fragment = resolved
            file_set = self._file_set if universe == "lessons" else self._site_file_set
            case_map = self._casefold_files if universe == "lessons" else self._casefold_site_files
            candidate = target
            if candidate.endswith("/"):
                candidate += "index.html"
            if candidate in file_set:
                if record.public_source and universe == "lessons" and self._is_public_path(candidate):
                    self.resolved_public_targets.add(candidate)
                if fragment and candidate in self.html and fragment not in self.html[candidate].ids:
                    self.add("warning", "reference", record.source, f"Fragment #{fragment} is absent in {candidate}", line=record.line, blocking=False)
                continue
            directory_index = candidate.rstrip("/") + "/index.html"
            if directory_index in file_set:
                if record.public_source and universe == "lessons" and self._is_public_path(directory_index):
                    self.resolved_public_targets.add(directory_index)
                continue
            folded = candidate.casefold()
            if folded in case_map:
                self.add("error", "reference", record.source, f"Case-mismatched local reference: {value}", line=record.line, details=f"Expected one of: {case_map[folded]}", blocking=record.public_source)
            else:
                label = "Lessons" if universe == "lessons" else "website"
                severity = "error" if record.public_source else "warning"
                self.add(severity, "reference", record.source, f"Missing local {label} target: {value}", line=record.line, details=target, blocking=record.public_source)

    def _resolve_reference(self, record: RefRecord) -> tuple[str, str, str] | None:
        raw = html_module.unescape(record.value.strip()).replace("\\", "/")
        if not raw or raw.startswith(("#", "//")):
            return None
        parsed = urllib.parse.urlsplit(raw)
        if parsed.scheme.lower() in KNOWN_EXTERNAL_SCHEMES:
            return None
        if parsed.scheme:
            return None
        source_virtual = "https://audit.invalid/Lessons/" + urllib.parse.quote(record.source, safe="/")
        joined = urllib.parse.urljoin(source_virtual, raw)
        target = urllib.parse.urlsplit(joined)
        path = urllib.parse.unquote(target.path)
        fragment = urllib.parse.unquote(target.fragment)
        if path == "/Lessons":
            return "lessons", "index.html", fragment
        if path.startswith("/Lessons/"):
            rel = posixpath.normpath(path[len("/Lessons/"):])
            if rel == ".":
                rel = "index.html"
            return "lessons", rel.lstrip("/"), fragment
        rel = posixpath.normpath(path.lstrip("/"))
        if rel == ".":
            rel = "index.html"
        return "site", rel, fragment

    def _check_site_repository(self) -> None:
        site_json_path = self.site_root / "site.json"
        if not site_json_path.exists():
            self.add("error", "site-config", "site.json", "Website site.json is missing")
            return
        try:
            site_data = json.loads(site_json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.add("error", "site-config", "site.json", "Website site.json is invalid", details=str(exc))
            return
        doors = site_data.get("doors") if isinstance(site_data, dict) else None
        if not isinstance(doors, list):
            self.add("error", "site-config", "site.json", "site.json has no doors array")
            doors = []
        lessons_doors = [door for door in doors if isinstance(door, dict) and door.get("zone") == "lessons"]
        lesson_hub = [door for door in lessons_doors if str(door.get("href", "")).strip("/") == "Lessons"]
        if len(lesson_hub) != 1:
            self.add("error", "site-config", "site.json", f"Expected exactly one Lesson Hub door to Lessons/; found {len(lesson_hub)}")
        elif not lesson_hub[0].get("countKey"):
            self.add("warning", "site-config", "site.json", "Lesson Hub door has no countKey", blocking=False)
        count_keys = [str(door.get("countKey")) for door in doors if isinstance(door, dict) and door.get("countKey")]
        for duplicate, count in Counter(count_keys).items():
            if count > 1:
                self.add("error", "site-config", "site.json", f"Duplicate door countKey: {duplicate}")
        loaders: list[str] = []
        lesson_refs: list[str] = []
        for rel in sorted(self._site_file_set):
            if pathlib.PurePosixPath(rel).suffix.lower() not in {".html", ".js", ".mjs", ".css", ".md"}:
                continue
            try:
                text = (self.site_root / rel).read_text(encoding="utf-8")
            except Exception:
                continue
            if "site.json" in text:
                loaders.append(rel)
            if "Lessons/" in text:
                lesson_refs.append(rel)
        if not loaders:
            self.add("error", "site-config", "site.json", "No website runtime/document references site.json")
        if not lesson_refs:
            self.add("error", "site-config", "site.json", "No website file references Lessons/")
        cname_path = self.site_root / "CNAME"
        cname = cname_path.read_text(encoding="utf-8").strip() if cname_path.exists() else ""
        if cname and cname.lower() != "madebymatt.uk":
            self.add("warning", "site-config", "CNAME", f"Unexpected custom domain: {cname}", blocking=False)
        self.site_checks = {
            "lesson_door_count": len(lesson_hub),
            "lessons_zone_door_count": len(lessons_doors),
            "site_json_loaders": loaders,
            "files_referencing_lessons": lesson_refs,
            "cname": cname,
        }

    def _browser_probe(self, modes: Sequence[str], page_timeout: float, settle: float) -> None:
        try:
            from selenium import webdriver  # type: ignore
            from selenium.common.exceptions import TimeoutException, WebDriverException  # type: ignore
        except Exception:
            return
        html_paths = sorted(self.html)
        if not html_paths:
            self.add("error", "browser", "<estate>", "No HTML files were available for browser probing")
            return
        server = CombinedServer(self.root, self.site_root)
        server.start()
        driver = None
        try:
            options = webdriver.ChromeOptions()
            chrome = next((shutil.which(name) for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(name)), None)
            if chrome:
                options.binary_location = chrome
            for arg in (
                "--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                "--disable-background-networking", "--disable-component-update", "--disable-default-apps",
                "--disable-features=Translate,BackForwardCache", "--autoplay-policy=no-user-gesture-required",
                "--window-size=1440,1000", "--remote-allow-origins=*", "--no-first-run",
            ):
                options.add_argument(arg)
            options.set_capability("goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"})
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(page_timeout)
            driver.set_script_timeout(max(10, int(page_timeout)))
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": ERROR_HOOK_JS})
            for mode in modes:
                self._configure_browser_mode(driver, mode)
                for index, rel in enumerate(html_paths, start=1):
                    public = self.html[rel].public
                    result: dict[str, Any] = {
                        "path": rel, "mode": mode, "public": public, "status": "unknown",
                        "errors": [], "warnings": [], "local_http_errors": [], "optional_http_failures": [], "interaction": None,
                    }
                    try:
                        with contextlib.suppress(Exception):
                            driver.get_log("browser")
                            driver.get_log("performance")
                        url = f"{server.origin}/Lessons/{urllib.parse.quote(rel, safe='/')}"
                        driver.get(url)
                        time.sleep(settle)
                        ready = driver.execute_script("return document.readyState")
                        result["ready_state"] = ready
                        result["title"] = driver.title
                        result["current_url"] = driver.current_url
                        surface = driver.execute_script(BROWSER_SURFACE_JS)
                        result.update(surface or {})
                        hook_errors = driver.execute_script("return window.__estateAuditErrors || []") or []
                        for error in hook_errors:
                            result["errors"].append({"kind": "window", "message": str(error)[:2000]})
                        browser_logs = driver.get_log("browser")
