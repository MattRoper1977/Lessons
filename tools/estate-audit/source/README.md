# Estate audit source set

The implementation is kept as ordered UTF-8 source segments (`00.inc`, `01.inc`,
...). `../estate_audit.py` concatenates them in lexical order, verifies the
assembled SHA-256 (`86837601c2efa7febc9e460f6bb4d7308ac75700dc96452b12b93d60fb5de31e`),
compiles the result and executes it in the module namespace. The segments are
plain source for review; any missing, reordered or edited segment fails before
the audit begins.
