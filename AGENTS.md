# Codex Project Instructions

This repo hosts standalone GitHub Pages product display pages for Canva Website links.

## Trigger Words

When Jason says `refresh` or `更新` in this project, treat it as a request to refresh the product pages from the Google Drive source folder.

Follow [docs/update-workflow.md](docs/update-workflow.md).

## Refresh Contract

Use Google Drive as the source of truth:

```text
https://drive.google.com/drive/folders/1tJDzPefoX8tVQqhUJyh-ppPTuJsTVJ0K
```

The local site source of truth is:

```text
tools/product_data.json
```

Manual Codex refresh flow:

1. List the Drive root folder and each child product folder, using the Google Drive connector when available.
2. Update `tools/product_data.json` with any added, removed, or renamed product images and folders.
3. Keep visible product codes extension-free.
4. Run `tools/refresh_site.py` with the bundled Python runtime.
5. Run `tools/verify_site.py`.
6. Commit and push the changes.
7. Confirm GitHub Pages build and live page status.

Do not hand-edit the generated `products/*.html` unless the generator cannot express the requested change. Prefer editing `tools/product_data.json`, `tools/build_product_pages.py`, or CSS, then regenerate.

## Scheduled Automation

GitHub Actions is the cloud automation path because it can run even when Jason's computer is shut down.

The workflow is:

```text
.github/workflows/refresh-products.yml
```

It runs every night at 00:00 Hong Kong time and can also be run manually from GitHub Actions. It requires one of these repository secrets:

```text
GOOGLE_DRIVE_API_KEY
GOOGLE_SERVICE_ACCOUNT_JSON
```

Use `GOOGLE_DRIVE_API_KEY` for public/shared source folders. Use `GOOGLE_SERVICE_ACCOUNT_JSON` for private folders shared with a service account. Use `GOOGLE_DRIVE_ACCESS_TOKEN` only as a temporary fallback. Do not commit credentials into this repo.
