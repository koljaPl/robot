# Before the 2026-10-25 price/stock review

These files preserve the prior EUR105.34 basket and entry documents. The previous
price regression is retained byte-for-byte as `tests/test_print_revision.py.txt`
so normal pytest discovery does not collect it as a second live module. The first
review test run exposed that duplicate-name collection issue; its failed log is
retained under validation/2026-10-25/procurement_review/pytest.txt. The source was
renamed, not deleted or changed; the rerun has a separate log.
