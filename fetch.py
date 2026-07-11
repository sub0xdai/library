#!/usr/bin/env python3
"""Generic book-fetch engine: download + merge. Site scraping lives in per-book scripts."""

import concurrent.futures
from pathlib import Path

import requests
from pypdf import PdfWriter


def download(urls: dict[int, str], output_dir: Path) -> None:
    """Download PDFs in parallel, skipping already-downloaded files."""
    output_dir.mkdir(exist_ok=True)

    def _fetch(idx: int, url: str) -> None:
        url = url.strip()
        filename = url.split("/")[-1]
        filepath = output_dir / f"{idx:03d}-{filename}"
        if filepath.exists():
            return
        try:
            res = requests.get(url, timeout=120)
            res.raise_for_status()
            filepath.write_bytes(res.content)
            print(f"  {filename}")
        except requests.RequestException as e:
            print(f"  FAILED {url}: {e}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(_fetch, idx, url) for idx, url in urls.items()]
        concurrent.futures.wait(futures)


def merge(output_dir: Path, output_pdf: Path, order: list[int] | None = None) -> None:
    """Merge downloaded PDFs. If *order* is given, it specifies chapter indices;
    otherwise merges in sorted glob order."""
    pdfs = sorted(output_dir.glob("*.pdf"))
    if not pdfs:
        return

    if order is not None:
        lookup = {int(p.name.split("-")[0]): p for p in pdfs}
        pdfs = [lookup[i] for i in order if i in lookup]

    merger = PdfWriter()
    for p in pdfs:
        merger.append(p)
    merger.write(output_pdf)
    merger.close()
    print(f"Merged → {output_pdf}")
