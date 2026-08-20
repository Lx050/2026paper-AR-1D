# Dataset Migration Record — 2026-08-19

## Purpose

Move the complete background-editing dataset asset tree from its previous remote workspace into the target research workspace while preserving usable content and producing reproducible integrity evidence.

This record contains validation metadata only. The dataset and its transfer archive are not committed to this repository.

## Source audit

- Regular files: 7,556
- Absolute symbolic links: 360
- Logical files when following links: 7,916
- Directories: 1,463
- Top-level asset groups: 5

All 360 symbolic links resolved successfully. Their targets were contained in the same logical dataset asset tree, but the stored absolute paths were specific to the previous workspace.

## Migration behavior

The transfer archive dereferenced the 360 workspace-specific symbolic links. The target therefore contains 7,916 directly readable files and no symbolic links. This makes the migrated copy self-contained and prevents broken references in the target workspace.

The temporary self-contained archive had the following integrity metadata:

```text
Size:   8,971,863,763 bytes
SHA256: d148ec64f9912d68e51bf7a5cc78f34c9d3cf4c4ec53e78b22c4a34002e7839f
```

## Validation result

The source logical tree and target physical tree were hashed by relative path and file content after migration.

```text
Source logical files: 7,916
Target files:         7,916
Source directories:   1,463
Target directories:   1,463
Tree SHA256:           c72b87db70805cd04c2e5ee204c7e6d258d2ba2ba0161d602437c341c235d5d3
Target symbolic links: 0
Ownership exceptions:  0
```

The matching tree hash verifies that every logical source path has the same file content at the target. Temporary remote archives were removed after validation.

## Repository boundary

This repository stores only the migration record. Large binary assets, local backup archives, remote host identifiers, account names, and machine-specific paths remain outside version control.
