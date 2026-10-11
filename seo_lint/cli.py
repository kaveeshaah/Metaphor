import argparse
import json
import sys
from dataclasses import asdict

from bs4 import BeautifulSoup

from .fetch import fetch_page
from .checks import ALL_CHECKS, check_response_time
from .links import check_links

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ICONS = {"pass": "✅", "warn": "⚠️ ", "fail": "❌"}


def run_audit(url: str):
    response = fetch_page(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = [check(soup) for check in ALL_CHECKS]
    results.append(check_response_time(response))
    results.append(check_links(soup, response.url))
    return results


def print_text(url, results):
    print(f"\nSEO report for {url}\n")
    for r in results:
        print(f"{ICONS[r.status]} {r.name}: {r.message}")


def print_json(url, results):
    report = {"url": url, "results": [asdict(r) for r in results]}
    print(json.dumps(report, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Audit a page's on-page SEO.")
    parser.add_argument("url", help="Page to audit, e.g. https://example.com")
    parser.add_argument(
        "--output", choices=["text", "json"], default="text",
        help="Report format (default: text)",
    )
    args = parser.parse_args()

    try:
        results = run_audit(args.url)
    except Exception as e:
        print(f"Could not audit {args.url}: {e}", file=sys.stderr)
        raise SystemExit(2)

    if args.output == "json":
        print_json(args.url, results)
    else:
        print_text(args.url, results)

    # Non-zero exit code if anything failed, like a real linter
    if any(r.status == "fail" for r in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()