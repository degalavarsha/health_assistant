"""Download the latest MedlinePlus health-topics XML (RAG knowledge base seed).

MedlinePlus requires attribution ("Source: MedlinePlus.gov") and its topic-page
images may not be redistributed; this script only fetches the XML text.

Usage:  python ingest/download_medlineplus.py [--out data/knowledge/medlineplus]
"""
import argparse
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

PAGE = "https://medlineplus.gov/xml.html"
UA = {"User-Agent": "ai-health-assistant-research"}


def get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(
        Path(__file__).resolve().parents[2] / "data" / "knowledge" / "medlineplus"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    html = get(PAGE).decode("utf8", "ignore")
    links = sorted(set(re.findall(r'href="([^"]*mplus_topics_compressed_[\d-]+\.zip)"', html)))
    if not links:
        print("No compressed topics file found on", PAGE)
        return 1
    url = links[-1]  # newest date sorts last
    print("Downloading", url)
    zpath = out / Path(url).name
    zpath.write_bytes(get(url))
    with zipfile.ZipFile(zpath) as z:
        z.extractall(out)
    zpath.unlink()
    print("Extracted:", ", ".join(sorted(p.name for p in out.iterdir())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
