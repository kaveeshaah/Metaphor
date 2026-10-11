# seo-lint

A command-line tool that audits a web page's on-page SEO and prints a
report, like a linter for your `<head>` and headings.

## What it checks

- Title tag (presence and length)
- Meta description (presence and length)
- H1 tag (exactly one)
- Heading order (no skipped levels)
- Image alt text
- Canonical tag
- Response time and HTML size
- Broken links (distinguishes dead links from sites that block bots)

## Install

    git clone <your-repo-url>
    cd seo-lint
    python -m venv venv
    venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
    pip install -e ".[dev]"

## Usage

    seo-lint https://example.com
    seo-lint https://example.com --output json

Exit codes: `0` no failures, `1` at least one failed check, `2` the page
could not be audited.

## Example output

    SEO report for https://example.com/

    ✅ Title tag: present (32 chars)
    ✅ Meta description: present (138 chars)
    ✅ H1 tag: present (23 chars)
    ⚠️  Canonical tag: missing
    ❌ Links: 1 of 3 broken: https://example.com/old (HTTP 404)

## Limitations

- Only reads the HTML the server sends. Pages rendered entirely by
  JavaScript may show missing tags.
- Response time measures server response, not full page load. For
  Core Web Vitals, use Google's PageSpeed Insights.

## Development

    pytest