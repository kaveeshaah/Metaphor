import argparse
from bs4 import BeautifulSoup

from .fetch import fetch_page
from .checks import ALL_CHECKS

ICONS = {"pass": "✅", "warn": "⚠️ ", "fail": "❌"}


def main():
    parser = argparse.ArgumentParser(description="Audit a page's on-page SEO.")
    parser.add_argument("url", help="Page to audit, e.g. https://example.com")
    args = parser.parse_args()

    try:
        response = fetch_page(args.url)
    except Exception as e:
        print(f"Could not fetch {args.url}: {e}")
        raise SystemExit(1)

    soup = BeautifulSoup(response.text, "html.parser")

    print(f"\nSEO report for {args.url}\n")
    for check in ALL_CHECKS:
        result = check(soup)
        print(f"{ICONS[result.status]} {result.name}: {result.message}")


if __name__ == "__main__":
    main()