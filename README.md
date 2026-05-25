# Shine Online Shop Specific Product Pages

This folder contains five standalone GitHub Pages product display pages for Canva Website links.

## Pages

- `products/masterpiece-cat-cloth.html`
- `products/dog-statue-cloth.html`
- `products/pop-up-world.html`
- `products/pop-up-festival.html`
- `products/pop-up-hong-kong.html`

## Link List

Use `docs/page-links.md` or `docs/page-links.docx` to copy the final page links into Canva.

GitHub Pages root URL:

```text
https://jasonwongkwanho.github.io/shine-online-shop-specific-products-pages/
```

## Image Access

The pages display local optimized WebP images generated from the Google Drive source files. The "open original image" links still point to Google Drive.

## Updating The Site

For manual updates, say `refresh` or `更新` in this project and follow `AGENTS.md`.

For direct local refresh after `tools/product_data.json` has been updated, run:

```powershell
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'tools\refresh_site.py'
```

See `docs/update-workflow.md` for the full future update workflow.

## Nightly GitHub Actions Refresh

The repo includes a GitHub Actions workflow at `.github/workflows/refresh-products.yml`.

It runs every night at 00:00 Hong Kong time, reads the Google Drive source folder, regenerates the local WebP images and product pages, verifies the output, and commits changes back to `main`.

To activate Drive reading in GitHub Actions, set one of these repository secrets:

```text
GOOGLE_DRIVE_API_KEY
GOOGLE_SERVICE_ACCOUNT_JSON
```

Use `GOOGLE_DRIVE_API_KEY` when the Drive folder/files are public or readable by the key. Use `GOOGLE_SERVICE_ACCOUNT_JSON` when the Drive folder is private; share the folder with the service account email. A temporary `GOOGLE_DRIVE_ACCESS_TOKEN` secret is also supported, but it is not ideal for scheduled use.
