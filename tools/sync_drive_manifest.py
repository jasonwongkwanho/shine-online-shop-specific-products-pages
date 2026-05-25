import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "tools" / "product_data.json"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3/files"
FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def natural_sort_key(value):
    parts = re.split(r"(\d+)", value.casefold())
    return [int(part) if part.isdigit() else part for part in parts]


def slugify(value, fallback):
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or fallback


def file_stem(name):
    return Path(name).stem


def read_manifest():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def write_manifest(data):
    DATA_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def access_token_from_service_account_json():
    raw_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw_json:
        return None

    from google.auth.transport.requests import Request as GoogleAuthRequest
    from google.oauth2 import service_account

    info = json.loads(raw_json)
    credentials = service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    credentials.refresh(GoogleAuthRequest())
    return credentials.token


class DriveClient:
    def __init__(self, api_key=None, access_token=None):
        self.api_key = api_key
        self.access_token = access_token
        if not self.api_key and not self.access_token:
            raise RuntimeError(
                "Missing Google Drive credentials. Set GOOGLE_DRIVE_API_KEY "
                "for public/shared folders, GOOGLE_SERVICE_ACCOUNT_JSON for "
                "private shared folders, or GOOGLE_DRIVE_ACCESS_TOKEN."
            )

    def list_children(self, folder_id):
        files = []
        page_token = None
        while True:
            params = {
                "q": f"'{folder_id}' in parents and trashed = false",
                "fields": "nextPageToken,files(id,name,mimeType,modifiedTime)",
                "pageSize": "1000",
                "orderBy": "name_natural",
                "supportsAllDrives": "true",
                "includeItemsFromAllDrives": "true",
            }
            if self.api_key:
                params["key"] = self.api_key
            if page_token:
                params["pageToken"] = page_token

            url = f"{DRIVE_API_BASE}?{urlencode(params)}"
            headers = {"Accept": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            request = Request(url, headers=headers)

            with urlopen(request, timeout=45) as response:
                payload = json.loads(response.read().decode("utf-8"))

            files.extend(payload.get("files", []))
            page_token = payload.get("nextPageToken")
            if not page_token:
                return files


def is_image_file(file_record):
    mime_type = file_record.get("mimeType", "")
    suffix = Path(file_record.get("name", "")).suffix.casefold()
    return mime_type.startswith("image/") or suffix in IMAGE_EXTENSIONS


def build_meta(title, count, existing_meta=None):
    if existing_meta:
        meta = list(existing_meta)
        if meta:
            meta[0] = f"共 {count} 款"
            return meta

    if "_" in title:
        category, series = title.split("_", 1)
        return [f"共 {count} 款", category, series]
    return [f"共 {count} 款", title]


def page_file_for_folder(folder, used_files, existing_file=None):
    if existing_file:
        return existing_file

    base = slugify(folder["name"], f"series-{folder['id'][:8]}")
    candidate = f"{base}.html"
    index = 2
    while candidate in used_files:
        candidate = f"{base}-{index}.html"
        index += 1
    return candidate


def sync_manifest(remove_missing_folders=False):
    data = read_manifest()
    root = data["drive_root"]
    client = DriveClient(
        api_key=os.getenv("GOOGLE_DRIVE_API_KEY"),
        access_token=os.getenv("GOOGLE_DRIVE_ACCESS_TOKEN") or access_token_from_service_account_json(),
    )

    root_children = client.list_children(root["folder_id"])
    folders = [
        item for item in root_children
        if item.get("mimeType") == FOLDER_MIME_TYPE
    ]
    folders.sort(key=lambda item: natural_sort_key(item["name"]))

    existing_by_id = {
        page.get("folder_id"): page
        for page in data.get("pages", [])
        if page.get("folder_id")
    }
    existing_by_title = {
        page.get("title"): page
        for page in data.get("pages", [])
        if page.get("title")
    }
    used_files = {page["file"] for page in data.get("pages", [])}
    synced_folder_ids = set()
    synced_pages = []

    for folder in folders:
        existing = existing_by_id.get(folder["id"]) or existing_by_title.get(folder["name"])
        page_file = page_file_for_folder(folder, used_files, existing_file=existing.get("file") if existing else None)
        used_files.add(page_file)

        folder_children = client.list_children(folder["id"])
        image_files = [item for item in folder_children if is_image_file(item)]
        image_files.sort(key=lambda item: natural_sort_key(file_stem(item["name"])))

        items = [
            {"code": file_stem(item["name"]), "drive_id": item["id"]}
            for item in image_files
        ]

        synced_pages.append({
            "file": page_file,
            "folder_id": folder["id"],
            "title": folder["name"],
            "meta": build_meta(folder["name"], len(items), existing.get("meta") if existing else None),
            "items": items,
        })
        synced_folder_ids.add(folder["id"])

    if not remove_missing_folders:
        for page in data.get("pages", []):
            folder_id = page.get("folder_id")
            if folder_id and folder_id not in synced_folder_ids:
                synced_pages.append(page)

    data["pages"] = synced_pages
    write_manifest(data)
    print(f"Synced {len(synced_pages)} page(s) from Google Drive.")


def main():
    parser = argparse.ArgumentParser(description="Sync product_data.json from Google Drive folders.")
    parser.add_argument(
        "--remove-missing-folders",
        action="store_true",
        help="Remove manifest pages when the corresponding Drive folder is not found.",
    )
    args = parser.parse_args()

    try:
        sync_manifest(remove_missing_folders=args.remove_missing_folders)
    except Exception as exc:
        print(f"Drive manifest sync failed: {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
