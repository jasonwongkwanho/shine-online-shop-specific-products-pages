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

Update `tools/product_data.json`, then run:

```powershell
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'tools\refresh_site.py'
```

See `docs/update-workflow.md` for the full future update workflow.
