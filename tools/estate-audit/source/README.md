# Estate audit source set

The implementation is kept as ordered UTF-8 source segments (`00.inc`, `01.inc`,
...). `../estate_audit.py` concatenates them in lexical order, verifies the
assembled SHA-256 (`175a1329af9adacb81583b0fc97b85ece4cdf39f454b6403c66bb48606b4f7c0`),
compiles the result and executes it in the module namespace. The segments are
plain source for review; any missing, reordered or edited segment fails before
the audit begins.
