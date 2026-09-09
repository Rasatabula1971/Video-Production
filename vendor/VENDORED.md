# Vendored dependencies

## openmontage

- **Upstream:** https://github.com/calesthio/openmontage
- **Commit:** `08e2151fa02de28a5d6a312b3d575692bf147ad7`
- **Date:** 2026-09-05
- **License:** AGPL-3.0 (`openmontage/LICENSE`)
- **Method:** vendored by copy (not a submodule). Self-contained, per `docs/PLAN_v1.md` §1.

### Why vendored by copy

This is a product, not a fork we intend to upstream. A copy keeps the repo
self-contained (no dependency on the upstream repo staying online) at the cost
of making upstream updates a manual re-vendor.

### What was removed from the copy

Three non-functional example media files (see `NOTICE`). Nothing else.

### We do not edit `openmontage/` in place

All project-specific behaviour lives in `montage_ext/` and `subjects/`. If a
change to openmontage itself ever becomes unavoidable, record it here with a
diff and a reason, so the next re-vendor can re-apply it.

### How to update the vendored copy

1. `git clone https://github.com/calesthio/openmontage` somewhere outside this repo.
2. Note the new HEAD commit.
3. Replace `vendor/openmontage/` contents (keep this file and `NOTICE` in sync).
4. Re-remove the large example media files.
5. Re-run the smoke checks in `BUILD_STATUS.md`.
6. Update the commit hash here, in `NOTICE`, and in `README.md`.
