# Estate audit source set

The implementation is kept as ordered UTF-8 source segments (`00.inc`, `01.inc`,
...). `../estate_audit.py` concatenates them in lexical order, verifies the
assembled SHA-256 (`91d8505540abec44964478248da62291b6d254d4b1b3620247aef98fd16fb197`),
compiles the result and executes it in the module namespace. The segments are
plain source for review; any missing, reordered or edited segment fails before
the audit begins.
