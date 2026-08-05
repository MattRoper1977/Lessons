                continue
            rel = path.relative_to(self.site_root).as_posix()
            self._site_file_set.add(rel)
            self._casefold_site_files[rel.casefold()].append(rel)
        try:
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.site_root, text=True).strip()
        except Exception:
            commit = "unknown"
        self.metrics["site_commit"] = commit
        self.metrics["site_file_count"] = len(self._site_file_set)
        for paths in self._casefold_site_files.values():
            if len(paths) > 1:
                self.add("warning", "site-config", paths[0], "Website repository has a case-insensitive path collision", details=" | ".join(paths), blocking=False)

    def _inventory_files(self, files: Sequence[pathlib.Path]) -> None:
        extension_counts: Counter[str] = Counter()
        total_bytes = 0
        zero_byte = 0
        for path in files:
            rel = path.relative_to(self.root).as_posix()
            try:
                stat = path.lstat()
                size = stat.st_size
            except OSError as exc:
                self.add("error", "filesystem", rel, "Cannot stat tracked file", details=str(exc))
                continue
            total_bytes += size
            ext = path.suffix.lower() or "<none>"
            extension_counts[ext] += 1
            if size == 0:
                zero_byte += 1
                self.add("warning", "content", rel, "Tracked file is zero bytes", blocking=False)
            sha = self._sha256_path(path) if path.is_file() else "symlink"
            public = self._is_public_path(rel)
            self.inventory.append({
                "path": rel,
                "size": size,
                "extension": ext,
                "public_candidate": public,
                "sha256": sha,
                "symlink": path.is_symlink(),
            })
            self._check_path_name(rel)
        self.metrics["tracked_bytes"] = total_bytes
        self.metrics["zero_byte_files"] = zero_byte
        self.metrics["extensions"] = dict(sorted(extension_counts.items()))
        self.metrics["largest_files"] = sorted(self.inventory, key=lambda row: row["size"], reverse=True)[:25]

    def _check_path_name(self, rel: str) -> None:
        for segment in pathlib.PurePosixPath(rel).parts:
            stem = segment.split(".", 1)[0].upper()
            if stem in WINDOWS_RESERVED:
                self.add("error", "path", rel, f"Path uses Windows-reserved name: {segment}")
            if segment.endswith(" ") or segment.endswith("."):
                self.add("error", "path", rel, f"Path segment has a trailing space or dot: {segment!r}")
            if any(ord(ch) < 32 for ch in segment):
                self.add("error", "path", rel, "Path contains a control character")
        if "\\" in rel:
            self.add("error", "path", rel, "Tracked path contains a backslash")

    def _validate_files(self, files: Sequence[pathlib.Path]) -> None:
        html_paths: list[pathlib.Path] = []
        js_paths: list[pathlib.Path] = []
        shell_paths: list[pathlib.Path] = []
        ext_counts = self.metrics.get("extensions", {})
        for path in files:
            rel = path.relative_to(self.root).as_posix()
            if path.is_symlink():
                self._validate_symlink(path, rel)
                continue
            ext = path.suffix.lower()
            try:
                data = path.read_bytes()
            except OSError as exc:
                self.add("error", "filesystem", rel, "Cannot read tracked file", details=str(exc))
                continue
            self._secret_scan(rel, data)
            if ext in IMAGE_EXTENSIONS:
                self._validate_image(path, rel)
                continue
            if ext == ".svg":
                self._validate_xml(path, rel, expect_svg=True)
                continue
            if ext == ".pdf":
                self._validate_pdf(path, rel)
                continue
            if ext in OFFICE_ZIP_EXTENSIONS or ext in ARCHIVE_EXTENSIONS:
                self._validate_zip(path, rel, office=ext in OFFICE_ZIP_EXTENSIONS)
                continue
            if ext in MEDIA_EXTENSIONS:
                self._validate_media(path, rel)
                continue
            if ext in FONT_EXTENSIONS:
                self._validate_font_signature(data, rel, ext)
                continue
            is_text = ext in TEXT_EXTENSIONS or self._looks_text(data)
            if not is_text:
                continue
            text = self._decode_text(rel, data)
            self._text_cache[rel] = text
            if "\x00" in text:
                self.add("error", "encoding", rel, "Text file contains NUL characters")
            if ext in {".html", ".htm"}:
                html_paths.append(path)
                self._validate_html(path, rel, text)
            elif ext == ".css":
                self._validate_css(rel, text)
            elif ext in {".json", ".webmanifest"}:
                self._validate_json(rel, text)
            elif ext == ".jsonl":
                self._validate_jsonl(rel, text)
            elif ext == ".toml":
                self._validate_toml(rel, text)
            elif ext in {".yml", ".yaml"}:
                self._validate_yaml(rel, text)
            elif ext == ".py":
                self._validate_python(rel, text)
            elif ext in {".xml"}:
                self._validate_xml(path, rel, expect_svg=False)
            elif ext == ".csv":
                self._validate_csv(rel, text, ",")
            elif ext == ".tsv":
                self._validate_csv(rel, text, "\t")
            if ext in {".js", ".mjs", ".cjs"}:
                js_paths.append(path)
            if ext in {".sh", ".bash"} or (not ext and text.startswith("#!") and "bash" in text.splitlines()[0]):
                shell_paths.append(path)
        # External script syntax is run after HTML parsing so module references are known.
        module_refs = self._module_script_targets()
        for path in js_paths:
            rel = path.relative_to(self.root).as_posix()
            self._validate_javascript_path(path, rel, rel in module_refs)
        for path in shell_paths:
            rel = path.relative_to(self.root).as_posix()
            self._validate_shell(path, rel)
        self.metrics["html_file_count"] = len(html_paths)
        self.metrics["public_html_count"] = sum(1 for record in self.html.values() if record.public)
        self.metrics["support_html_count"] = sum(1 for record in self.html.values() if not record.public)
        self.metrics["script_file_count"] = len(js_paths)
        self.metrics["shell_file_count"] = len(shell_paths)
        self.metrics["format_extension_counts"] = ext_counts

    def _validate_symlink(self, path: pathlib.Path, rel: str) -> None:
        try:
            target = os.readlink(path)
        except OSError as exc:
            self.add("error", "filesystem", rel, "Cannot read symlink", details=str(exc))
            return
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError:
            self.add("error", "filesystem", rel, "Symlink escapes the repository", details=target)
            return
        if not resolved.exists():
            self.add("error", "filesystem", rel, "Symlink target is missing", details=target)

    def _secret_scan(self, rel: str, data: bytes) -> None:
        if len(data) > 5_000_000 or b"\x00" in data[:4096]:
            return
        text = data.decode("utf-8", "ignore")
        for name, pattern in SECRET_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                self.add("error", "secret", rel, f"Potential {name} committed", line=line)
        name = pathlib.PurePosixPath(rel).name.lower()
        if name in {".env", ".env.local", "id_rsa", "id_ed25519"} or name.endswith((".pem", ".key", ".p12", ".pfx")):
            self.add("error", "secret", rel, "Sensitive credential/key filename is tracked")

    def _validate_image(self, path: pathlib.Path, rel: str) -> None:
        ext = path.suffix.lower()
        data = path.read_bytes()[:64]
        if ext == ".avif" and not (b"ftypavif" in data or b"ftypavis" in data):
            self.add("error", "image", rel, "AVIF signature does not match the extension")
            return
        if Image is None:
            return
        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            # Pillow builds do not always ship an AVIF decoder. A valid ISO-BMFF
            # AVIF signature still proves that the tracked file is not random bytes;
            # browser/live probes provide the independent render check.
            if ext == ".avif" and (b"ftypavif" in data or b"ftypavis" in data):
                self.add(
                    "info", "image", rel,
                    "AVIF signature is valid but the runner decoder could not open it",
                    details=str(exc), blocking=False,
                )
                return
            self.add("error", "image", rel, "Image cannot be decoded", details=str(exc))

    def _validate_pdf(self, path: pathlib.Path, rel: str) -> None:
        data = path.read_bytes()
        if not data.startswith(b"%PDF-"):
            self.add("error", "pdf", rel, "PDF signature is missing")
            return
        if b"%%EOF" not in data[-4096:]:
            self.add("warning", "pdf", rel, "PDF EOF marker is not present near the end", blocking=False)
        if PdfReader is None:
            return
        try:
            reader = PdfReader(str(path), strict=False)
            count = len(reader.pages)
            if count == 0:
                self.add("error", "pdf", rel, "PDF has no pages")
        except Exception as exc:
            self.add("error", "pdf", rel, "PDF parser could not read the document", details=str(exc))

    def _validate_zip(self, path: pathlib.Path, rel: str, office: bool) -> None:
        ext = path.suffix.lower()
        try:
            with zipfile.ZipFile(path) as archive:
                bad = archive.testzip()
                if bad:
                    self.add("error", "archive", rel, "Archive contains a corrupt member", details=bad)
                names = set(archive.namelist())
                if ext in {".docx", ".xlsx", ".pptx"} and "[Content_Types].xml" not in names:
                    self.add("error", "archive", rel, "OOXML archive lacks [Content_Types].xml")
                elif ext in {".odt", ".ods", ".odp"}:
                    expected = {
                        ".odt": "application/vnd.oasis.opendocument.text",
                        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
                        ".odp": "application/vnd.oasis.opendocument.presentation",
                    }[ext]
                    if "mimetype" not in names:
                        self.add("error", "archive", rel, "OpenDocument archive lacks mimetype")
                    else:
                        actual = archive.read("mimetype").decode("ascii", "replace").strip()
                        if actual != expected:
                            self.add("error", "archive", rel, "OpenDocument mimetype does not match the extension", details=f"expected {expected}; got {actual}")
                elif ext == ".epub":
                    if "mimetype" not in names:
                        self.add("error", "archive", rel, "EPUB archive lacks mimetype")
                    else:
                        actual = archive.read("mimetype").decode("ascii", "replace").strip()
                        if actual != "application/epub+zip":
                            self.add("error", "archive", rel, "EPUB mimetype is invalid", details=actual)
                elif office and ext not in OFFICE_ZIP_EXTENSIONS:
                    self.add("warning", "archive", rel, "Unknown office-style archive extension", blocking=False)
                if not names:
                    self.add("warning", "archive", rel, "Archive is empty", blocking=False)
        except Exception as exc:
            self.add("error", "archive", rel, "Archive cannot be opened", details=str(exc))

    def _validate_media(self, path: pathlib.Path, rel: str) -> None:
        ffprobe = shutil.which("ffprobe")
        if not ffprobe:
            self.add("info", "media", rel, "ffprobe unavailable; media container was inventoried but not decoded", blocking=False)
            return
        proc = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration,format_name", "-of", "json", str(path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30, check=False,
        )
        if proc.returncode != 0:
            self.add("error", "media", rel, "Media file cannot be probed", details=proc.stderr.strip())

    def _validate_font_signature(self, data: bytes, rel: str, ext: str) -> None:
        signatures = {
            ".woff": (b"wOFF",), ".woff2": (b"wOF2",), ".ttf": (b"\x00\x01\x00\x00", b"true", b"typ1"),
            ".otf": (b"OTTO",), ".eot": tuple(),
        }
        allowed = signatures.get(ext, tuple())
        if allowed and not any(data.startswith(sig) for sig in allowed):
            self.add("error", "font", rel, f"{ext} signature does not match the extension")

    def _validate_xml(self, path: pathlib.Path, rel: str, expect_svg: bool) -> None:
        import xml.etree.ElementTree as ET
        try:
            root = ET.parse(path).getroot()
            if expect_svg and not root.tag.lower().endswith("svg"):
                self.add("error", "svg", rel, "SVG file does not have an <svg> root element")
        except Exception as exc:
            self.add("error", "xml", rel, "XML/SVG is not well formed", details=str(exc))

    def _validate_json(self, rel: str, text: str) -> None:
        try:
            json.loads(text)
