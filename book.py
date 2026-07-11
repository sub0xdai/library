#!/usr/bin/env python3
"""OSTEP (Operating Systems: Three Easy Pieces) — scraper + config."""

from pathlib import Path

import bs4
import requests

from fetch import download, merge

BASE_URL = "http://pages.cs.wisc.edu/~remzi/OSTEP"
OUTPUT_DIR = Path("output")
OUTPUT_PDF = Path("operating-systems/operating-systems-three-easy-pieces.pdf")


def scrape() -> dict[int, str]:
    resp = requests.get(f"{BASE_URL}/#book-chapters", timeout=15)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, "html.parser")

    urls = {}
    for td in soup.find_all("td"):
        small = td.find("small")
        a = td.find("a")
        if small and a and "href" in a.attrs:
            try:
                idx = 100 + int(small.get_text(strip=True))
            except ValueError:
                continue
            urls[idx] = f"{BASE_URL}/{a.attrs['href']}"

    return urls


def merge_order(urls: dict[int, str]) -> list[int]:
    """OSTEP reorder: last 2 chapters moved to front (prefaces/appendices)."""
    keys = sorted(urls)
    return keys[-2:] + keys[:-2]


if __name__ == "__main__":
    urls = scrape()
    print(f"Found {len(urls)} chapters")
    download(urls, OUTPUT_DIR)
    merge(OUTPUT_DIR, OUTPUT_PDF, order=merge_order(urls))
