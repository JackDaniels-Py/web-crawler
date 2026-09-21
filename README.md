# Simple Web Crawler

A basic web crawler built with Python, `requests`, and `BeautifulSoup`. It was made as a learning project to practice web scraping, HTML parsing, and basic reconnaissance techniques.

The crawler targets [books.toscrape.com](http://books.toscrape.com), a website built specifically for scraping practice.

## What it does

- Sends GET requests to pages and follows internal links (up to a limit of 10 pages)
- Prints response headers for each page (basic recon)
- Extracts and prints the page title
- Extracts `<meta>` tags (name/content)
- Separates found links into internal and external
- Finds all `<form>` elements on the page and extracts:
  - method and action
  - input/textarea/select/button fields (name and type)
  - hidden fields
- Logs each step of the process (info, debug, warnings, errors)

## How to run

```bash
pip install requests beautifulsoup4
python recon2.py
```

## Notes

This is a learning project, not a polished tool. The code isn't organized into functions/classes yet, everything runs top-to-bottom in a single script. Next steps I'm considering:

- Breaking the logic into functions
- Adding command-line arguments (target URL, page limit)
- Exporting results to a file (JSON/CSV) instead of just printing

## Disclaimer

This script was built and tested only against `books.toscrape.com`, a site made for scraping practice. Don't run it against sites you don't have permission to scan.
