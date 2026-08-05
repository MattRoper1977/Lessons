        except json.JSONDecodeError as exc:
            self.add("error", "json", rel, "Invalid JSON", line=exc.lineno, details=exc.msg)

    def _validate_jsonl(self, rel: str, text: str) -> None:
        records = 0
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            records += 1
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                self.add("error", "json", rel, "Invalid JSON Lines record", line=line_number, details=exc.msg)
        if records == 0 and text.strip():
            self.add("warning", "json", rel, "JSON Lines file contains no records", blocking=False)

    def _validate_toml(self, rel: str, text: str) -> None:
        try:
            tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            line = getattr(exc, "lineno", None)
            self.add("error", "toml", rel, "Invalid TOML", line=line, details=str(exc))

    def _validate_yaml(self, rel: str, text: str) -> None:
        if yaml is None:
            return
        try:
            list(yaml.safe_load_all(text))
        except Exception as exc:
            line = getattr(getattr(exc, "problem_mark", None), "line", None)
            self.add("error", "yaml", rel, "Invalid YAML", line=(line + 1) if line is not None else None, details=str(exc))

    def _validate_python(self, rel: str, text: str) -> None:
        try:
            ast.parse(text, filename=rel)
        except SyntaxError as exc:
            self.add("error", "python", rel, "Python syntax error", line=exc.lineno, details=exc.msg)

    def _validate_csv(self, rel: str, text: str, delimiter: str) -> None:
        try:
            rows = list(csv.reader(io.StringIO(text), delimiter=delimiter))
        except csv.Error as exc:
            self.add("error", "csv", rel, "CSV/TSV parser error", details=str(exc))
            return
        widths = Counter(len(row) for row in rows if row)
        if len(widths) > 1:
            self.add("warning", "csv", rel, "Rows have inconsistent column counts", details=str(dict(widths)), blocking=False)

    def _validate_shell(self, path: pathlib.Path, rel: str) -> None:
        proc = subprocess.run(["bash", "-n", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if proc.returncode:
            self.add("error", "shell", rel, "Shell syntax error", details=proc.stderr.strip())

    def _validate_javascript_path(self, path: pathlib.Path, rel: str, force_module: bool) -> None:
        if not shutil.which("node"):
            return
        text = self._text_cache.get(rel)
        if text is None:
            text = self._decode_text(rel, path.read_bytes())
        module_hint = force_module or path.suffix.lower() == ".mjs" or bool(re.search(r"(?m)^\s*(?:import\s|export\s)", text))
        if module_hint and path.suffix.lower() != ".mjs":
            self._node_check_text(rel, text, module=True)
            return
        proc = subprocess.run(["node", "--check", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if proc.returncode:
            self.add("error", "javascript", rel, "JavaScript syntax error", details=self._clean_node_error(proc.stderr, rel))

    def _node_check_text(self, rel: str, text: str, module: bool, line_offset: int = 0, label: str = "inline script") -> None:
        if not shutil.which("node"):
            return
        suffix = ".mjs" if module else ".js"
        with tempfile.NamedTemporaryFile("w", suffix=suffix, encoding="utf-8", delete=False) as handle:
            handle.write(text)
            temp = pathlib.Path(handle.name)
        try:
            proc = subprocess.run(["node", "--check", str(temp)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if proc.returncode:
                detail = proc.stderr.replace(str(temp), rel)
                match = re.search(rf"{re.escape(rel)}:(\d+)", detail)
                line = int(match.group(1)) + line_offset if match else None
                self.add("error", "javascript", rel, f"JavaScript syntax error in {label}", line=line, details=self._clean_node_error(detail, rel))
        finally:
            with contextlib.suppress(OSError):
                temp.unlink()

    @staticmethod
    def _clean_node_error(stderr: str, rel: str) -> str:
        lines = [line.rstrip() for line in stderr.strip().splitlines()]
        return "\n".join(lines[-12:]).replace("file://", "")

    def _validate_css(self, rel: str, text: str, line_offset: int = 0, label: str = "stylesheet") -> None:
        if tinycss2 is None:
            return
        try:
            tokens = tinycss2.parse_stylesheet(text, skip_comments=False, skip_whitespace=False)
        except Exception as exc:
            self.add("error", "css", rel, f"CSS parser failed for {label}", details=str(exc))
            return
        for token in self._walk_css_tokens(tokens):
            if getattr(token, "type", None) == "error":
                line = getattr(token, "source_line", None)
                if line is not None:
                    line += line_offset
                self.add("error", "css", rel, f"CSS parse error in {label}", line=line, details=getattr(token, "message", None))
        for value, line in self._extract_css_urls(text, line_offset):
            self.references.append(RefRecord(rel, "css-url", value, line, self._is_public_path(rel)))

    def _walk_css_tokens(self, tokens: Iterable[Any]) -> Iterator[Any]:
        for token in tokens:
            yield token
            content = getattr(token, "content", None)
            if content:
                yield from self._walk_css_tokens(content)
            arguments = getattr(token, "arguments", None)
            if arguments:
                yield from self._walk_css_tokens(arguments)

    @staticmethod
    def _extract_css_urls(text: str, line_offset: int = 0) -> list[tuple[str, int]]:
        results: list[tuple[str, int]] = []
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", text, re.I | re.S):
            value = match.group(2).strip()
            if value:
                results.append((value, text.count("\n", 0, match.start()) + 1 + line_offset))
        return results

    def _validate_html(self, path: pathlib.Path, rel: str, text: str) -> None:
        public = self._is_public_path(rel)
        ids: list[str] = []
        refs: list[RefRecord] = []
        title = ""
        lang = ""
        has_viewport = False
        visible_controls = 0
        unnamed_controls = 0
        doc = None
        if html5lib is not None:
            try:
                parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("etree"), namespaceHTMLElements=False)
                doc = parser.parse(text)
                for position, code, data in parser.errors:
                    line = position[0] if position else None
                    severity = "error" if code in SEVERE_HTML5_CODES else "warning"
                    self.add(severity, "html", rel, f"HTML5 parse issue: {code}", line=line, details=json.dumps(data, ensure_ascii=False), blocking=severity == "error" and public)
            except Exception as exc:
                self.add("error", "html", rel, "HTML parser failed", details=str(exc), blocking=public)
        if doc is not None:
            for element in doc.iter():
                tag = str(element.tag).split("}")[-1].lower()
                attrs = {str(k).split("}")[-1].lower(): str(v) for k, v in element.attrib.items()}
                if tag == "html":
                    lang = attrs.get("lang", "").strip()
                if tag == "title":
                    title = "".join(element.itertext()).strip()
                if tag == "meta" and attrs.get("name", "").lower() == "viewport":
                    has_viewport = True
                if "id" in attrs:
                    ids.append(attrs["id"])
                line = self._find_attribute_line(text, attrs.get("id") or attrs.get("href") or attrs.get("src"))
                for attr in URL_ATTRS:
                    value = attrs.get(attr)
                    if value:
                        record = RefRecord(rel, attr, html_module.unescape(value).strip(), line, public)
                        refs.append(record)
                        self.references.append(record)
                srcset = attrs.get("srcset")
                if srcset:
                    for candidate in self._parse_srcset(srcset):
                        record = RefRecord(rel, "srcset", candidate, line, public)
                        refs.append(record)
                        self.references.append(record)
                if "style" in attrs and attrs["style"].strip():
                    self._validate_inline_style(rel, attrs["style"], line)
                for attr, value in attrs.items():
                    if attr.startswith("on") and value.strip():
                        wrapped = f"function __handler(event){{\n{value}\n}}\n"
                        self._node_check_text(rel, wrapped, module=False, line_offset=max((line or 1) - 2, 0), label=f"{attr} handler")
                if tag in {"button", "a", "input", "select", "textarea"}:
                    if self._element_is_control(tag, attrs):
                        visible_controls += 1
                        if not self._element_accessible_name(element, tag, attrs):
                            unnamed_controls += 1
                            self.add("warning", "accessibility", rel, f"Potentially unnamed {tag} control", line=line, blocking=False)
                if tag == "img" and "alt" not in attrs and attrs.get("aria-hidden") != "true" and attrs.get("role") not in {"presentation", "none"}:
                    self.add("warning", "accessibility", rel, "Image has no alt attribute", line=line, blocking=False)
                if tag == "iframe" and not (attrs.get("title") or attrs.get("aria-label")):
                    self.add("warning", "accessibility", rel, "Iframe has no title/aria-label", line=line, blocking=False)
                if tag == "a" and attrs.get("target", "").lower() == "_blank":
                    rel_tokens = set(attrs.get("rel", "").lower().split())
                    if "noopener" not in rel_tokens:
                        self.add("warning", "security", rel, "target=_blank link lacks rel=noopener", line=line, blocking=False)
        duplicate_ids = sorted(name for name, count in Counter(ids).items() if name and count > 1)
        for duplicate in duplicate_ids:
            self.add("error", "html", rel, f"Duplicate id: {duplicate}", blocking=public)
        has_doctype = bool(re.match(r"\s*<!doctype\s+html\b", text, re.I))
        if public and not has_doctype:
            self.add("warning", "html", rel, "Public HTML has no HTML5 doctype", blocking=False)
        if public and not title:
            self.add("warning", "accessibility", rel, "Public HTML has no non-empty <title>", blocking=False)
        if public and not lang:
            self.add("warning", "accessibility", rel, "Public HTML has no <html lang>", blocking=False)
        if public and not has_viewport:
            self.add("warning", "responsive", rel, "Public HTML has no viewport meta tag", blocking=False)
        self._validate_inline_blocks(rel, text)
        self.html[rel] = HtmlRecord(
            path=rel,
            ids=set(ids),
            duplicate_ids=duplicate_ids,
            refs=refs,
            public=public,
            title=title,
            lang=lang,
            has_viewport=has_viewport,
            has_doctype=has_doctype,
            reduced_motion_declared="prefers-reduced-motion" in text,
            visible_control_count=visible_controls,
            unnamed_control_count=unnamed_controls,
        )

    def _validate_inline_blocks(self, rel: str, text: str) -> None:
        script_pattern = re.compile(r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script\s*>", re.I | re.S)
        for match in script_pattern.finditer(text):
            attrs = self._parse_attrs(match.group("attrs"))
            if attrs.get("src"):
                continue
            script_type = attrs.get("type", "").strip().lower()
            if script_type in NON_JS_SCRIPT_TYPES or (script_type not in SCRIPT_TYPES and script_type):
                if "json" in script_type:
                    body = match.group("body").strip()
                    if body:
                        try:
                            json.loads(body)
                        except json.JSONDecodeError as exc:
                            line = text.count("\n", 0, match.start("body")) + exc.lineno
                            self.add("error", "json", rel, f"Invalid JSON in <script type={script_type}>", line=line, details=exc.msg, blocking=self._is_public_path(rel))
                continue
            body = match.group("body")
            if not body.strip():
                continue
            line_offset = text.count("\n", 0, match.start("body"))
            self._node_check_text(rel, body, module=script_type == "module", line_offset=line_offset, label="inline <script>")
        style_pattern = re.compile(r"<style\b[^>]*>(?P<body>.*?)</style\s*>", re.I | re.S)
        for match in style_pattern.finditer(text):
            body = match.group("body")
            line_offset = text.count("\n", 0, match.start("body"))
            self._validate_css(rel, body, line_offset=line_offset, label="inline <style>")

    def _validate_inline_style(self, rel: str, value: str, line: int | None) -> None:
        if tinycss2 is None:
            return
        try:
            tokens = tinycss2.parse_declaration_list(value, skip_comments=False, skip_whitespace=False)
            for token in self._walk_css_tokens(tokens):
                if getattr(token, "type", None) == "error":
                    self.add("error", "css", rel, "CSS parse error in style attribute", line=line, details=getattr(token, "message", None), blocking=self._is_public_path(rel))
        except Exception as exc:
            self.add("error", "css", rel, "CSS parser failed for style attribute", line=line, details=str(exc), blocking=self._is_public_path(rel))
        for url, _ in self._extract_css_urls(value):
            self.references.append(RefRecord(rel, "style-url", url, line, self._is_public_path(rel)))

    @staticmethod
    def _element_is_control(tag: str, attrs: dict[str, str]) -> bool:
        if tag == "a":
            return bool(attrs.get("href") or attrs.get("role") == "button")
        if tag == "input":
            return attrs.get("type", "text").lower() not in {"hidden"}
        return True

    @staticmethod
    def _element_accessible_name(element: Any, tag: str, attrs: dict[str, str]) -> str:
        for key in ("aria-label", "title", "alt", "value"):
            if attrs.get(key, "").strip():
                return attrs[key].strip()
        text = " ".join(part.strip() for part in element.itertext() if part.strip())
        if text:
            return text
        if attrs.get("aria-labelledby"):
            return attrs["aria-labelledby"]
        if tag == "select":
            return "select-options" if list(element) else ""
