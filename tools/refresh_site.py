import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script_name):
    script = ROOT / "tools" / script_name
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)


def main():
    run("optimize_product_images.py")
    run("build_product_pages.py")
    run("build_page_links_docx.py")
    print("Site refreshed: images optimized, pages rebuilt, DOCX link table regenerated.")


if __name__ == "__main__":
    main()
