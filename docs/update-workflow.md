# 更新產品展示頁流程

本專案已改成可重複刷新流程。日後新增、刪除或更換 Google Drive 圖片時，不需要手改 HTML。

## 主要檔案

- `tools/product_data.json`：5 個產品頁的資料來源，包括頁面名稱、系列資料、編號、Google Drive file ID。
- `tools/optimize_product_images.py`：下載 Drive 縮圖，輸出本地 WebP 圖片。
- `tools/build_product_pages.py`：根據 `product_data.json` 重建 `products/*.html`。
- `tools/build_page_links_docx.py`：重建 `docs/page-links.docx`。
- `tools/refresh_site.py`：一次過執行圖片壓縮、頁面重建、連結 DOCX 重建。

## 日後更新步驟

1. 先用 Google Drive connector 讀取主 folder 及各子 folder 圖片清單。
2. 按 Drive 最新清單更新 `tools/product_data.json`：
   - `code` 填展示用「編號」，不要包含 `.png`、`.JPEG` 等副檔名。
   - `drive_id` 填 Google Drive file ID。
   - `meta` 的「共 N 款」要跟該頁 items 數量一致。
3. 執行：

```powershell
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'tools\refresh_site.py'
```

4. 驗證：
   - 5 個 `products/*.html` 都有正確「編號」。
   - `assets/images/` 有對應的 `480/720/960.webp`。
   - HTML 不應再出現 `drive.google.com/thumbnail` 作為圖片來源；只保留「開啟原圖」的 Drive link。
5. Commit and push：

```powershell
git add assets/images products docs tools README.md
git commit -m "Update product pages"
git push
```

## 為甚麼這樣較快

舊做法是每次由訪客瀏覽器直接向 Google Drive 載入圖片縮圖。新做法是先把圖片轉成 GitHub Pages 本地 WebP，頁面載入時直接由同一個網站讀圖，減少跨站連線，也令檔案更細。

每張產品圖目前會輸出三個尺寸：

- `480.webp`：手機或細卡片
- `720.webp`：預設顯示
- `960.webp`：較大螢幕備用

頁面用 `srcset` 和 `sizes` 自動選合適圖片，第一張圖優先載入，其餘用 lazy loading。
