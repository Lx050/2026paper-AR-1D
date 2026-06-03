# Dataset Releases

## dataset-subject-background-v2026.06.03

Subject-consistent background editing dataset release.

Asset package:

```text
dataset_subject_background-v2026.06.03.tar.zst
```

Package contents:

- 120 accepted source/target background-edit triples.
- 120 subject mask/bbox annotations for the base set.
- 48 coverage-extension samples.
- 50 negative samples.
- 100 COCO val2017 real-validation samples.
- Metadata, QC notes, and generation/validation scripts.

Validation evidence:

```text
Final accepted rows: 120
Rejected rows: 0
VALIDATION_OK

Base rows with mask/bbox: 120
Coverage extension rows: 48
Negative rows: 50
Real validation rows: 100
EXTENDED_VALIDATION_OK
```

Archive audit:

```text
Packaged files: 1344
Excluded from archive: dataset_subject_background/.cache, __pycache__
SHA256: e0e99f52c4b904f5fad25330ef9b33113e80c22cb1ff4a405c022a162afd3fd0
```

Use the accompanying manifest asset to verify per-file SHA256 values after extraction.
