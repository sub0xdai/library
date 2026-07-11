# library

## Book fetcher

Generic engine for scraping, downloading, and merging chapter PDFs into a single book.

```
fetch.py        # Generic engine: download(urls, dir) + merge(dir, pdf, order=None)
book.py         # OSTEP scraper — example of a per-book script
```

### Adding a new book

1. Copy `book.py` to `some_book.py`
2. Replace `scrape()` with site-specific HTML parsing — return `dict[int, str]` mapping chapter indices to PDF URLs
3. Set `OUTPUT_DIR`, `OUTPUT_PDF`, and optionally a `merge_order()` if chapters need reordering
4. Run: `uv run python some_book.py`

The engine handles parallel download with resume (skips already-downloaded files) and PDF merge.
