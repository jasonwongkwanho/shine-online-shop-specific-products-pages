from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCT_DIR = ROOT / "products"

ORDER_NOTE = "請先在對話紀錄中記下心儀款式的編號，再到訂購表格相應欄位填寫「編號」及「購買數量」。"

PAGES = [
    {
        "file": "masterpiece-cat-cloth.html",
        "title": "眼鏡布_名畫喵系列",
        "meta": ["共 12 款", "眼鏡布", "名畫喵系列"],
        "items": [
            ("A01_CP", "1Ec_1FQVQiZTE1N3FfUVthatOAXK7ZI-_"),
            ("A01_MC", "1c7aLFLTw3E1UbZakghMGusFYdztb8S_x"),
            ("A02_CP", "14hUxKvIvRciNcDE2Dm3_yVui-zXQv9MQ"),
            ("A03_CP", "1ZkE-tQA1iZuOBUZEl48dhN7LgQwx-DVy"),
            ("A04_CP", "1lLvFOf8McjlNsKKqSW1h2L6rWwcSK9wr"),
            ("A05_CP", "1etdkgKwcrpHS6j0nSUbxdXcWHSfvuK9O"),
            ("A06_CP", "1otch2H260TkLZggE_H0xuKC4t5CvN6VT"),
            ("A07_CP", "1VA90CT3GZtNn_7s6mcH24YlUigbv0Bl-"),
            ("A08_CP", "16_9TsVO23XpgemMd1vTvxdO6LkKXpsga"),
            ("A09_CP", "1r57hXBGmUHCgr7MlgWogM2oz8vvIW2I1"),
            ("A10_CP", "1WRAaD8cUTOsExMiZR5Y52GM8DFcFHZNn"),
            ("A11_CP", "11Pr3ZVOiiAs5LNxp8wSEK1r2pe5rFV9x"),
        ],
    },
    {
        "file": "dog-statue-cloth.html",
        "title": "眼鏡布_犬雕像系列",
        "meta": ["共 2 款", "眼鏡布", "犬雕像系列"],
        "items": [
            ("C01_SE", "1ZKdz4xi5iuil9GW5DLQTcfWreH4Chaj1"),
            ("C01_VE", "1BVn_qpqqgfuqxQIBD3KEjVcK8wQBQ85X"),
        ],
    },
    {
        "file": "pop-up-world.html",
        "title": "立體咭_環球系列",
        "meta": ["共 1 款", "立體咭", "環球系列"],
        "items": [
            ("JP001", "15fBKXhg9xjUx8T9e4Iz_Sk_leyg25D7w"),
        ],
    },
    {
        "file": "pop-up-festival.html",
        "title": "立體咭_節慶系列",
        "meta": ["共 1 款", "立體咭", "節慶系列"],
        "items": [
            ("C001", "1KcQx_wLYAO2mSXdhOvxDr4KD0D8RMkBy"),
        ],
    },
    {
        "file": "pop-up-hong-kong.html",
        "title": "立體咭_港式情懷",
        "meta": ["共 3 款", "立體咭", "港式情懷"],
        "items": [
            ("001", "14ZuzdbA-08R_EZmy2l-pyna-ySZTKgMh"),
            ("002", "13vHGFDJuGKwp1izShN8tj4bB4dXyU_HI"),
            ("003", "1Q7eT2L-KydY_8w2eKAGe0IjszjD2waBQ"),
        ],
    },
]


def image_url(file_id):
    return f"https://drive.google.com/thumbnail?id={file_id}&sz=w1600"


def original_url(file_id):
    return f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"


def render_page(page):
    meta = "\n".join(f"        <li>{escape(value)}</li>" for value in page["meta"])
    cards = []
    for code, file_id in page["items"]:
        cards.append(
            f"""      <article class="product-card">
        <div class="image-frame">
          <img src="{image_url(file_id)}" alt="{escape(code)}" loading="lazy">
        </div>
        <div class="product-info">
          <p class="code-label">編號</p>
          <p class="product-code">{escape(code)}</p>
          <a class="original-link" href="{original_url(file_id)}" target="_blank" rel="noopener">開啟原圖</a>
        </div>
      </article>"""
        )
    gallery = "\n".join(cards)
    title = escape(page["title"])
    note = escape(ORDER_NOTE)
    return f"""<!doctype html>
<html lang="zh-Hant-HK">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
  <main class="page-shell">
    <header class="product-header">
      <p class="brand-line">網尚店</p>
      <h1>{title}</h1>
      <ul class="series-meta" aria-label="系列資料">
{meta}
      </ul>
    </header>

    <section class="order-note" aria-label="訂購提示">
      <p>{note}</p>
    </section>

    <section class="gallery" aria-label="產品圖片及編號">
{gallery}
    </section>
  </main>
</body>
</html>
"""


def main():
    PRODUCT_DIR.mkdir(exist_ok=True)
    for page in PAGES:
        (PRODUCT_DIR / page["file"]).write_text(render_page(page), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
