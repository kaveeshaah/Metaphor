from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urldefrag, urlparse

import requests

from .checks import Result

HEADERS = {"User-Agent": "seo-lint/0.1 (learning project)"}
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "#")


def collect_links(soup, base_url: str) -> list[str]:
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith(SKIP_PREFIXES):
            continue
        absolute, _fragment = urldefrag(urljoin(base_url, href))
        if urlparse(absolute).scheme in ("http", "https"):
            links.add(absolute)
    return sorted(links)


BLOCKED_CODES = {401, 403, 429, 999}


def check_one(url: str, timeout: int = 8):
    """Return (url, kind, detail). kind is 'ok', 'blocked', or 'broken'."""
    try:
        r = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if r.status_code in (403, 405, 501):
            r = requests.get(url, headers=HEADERS, timeout=timeout, stream=True)

        if r.status_code in BLOCKED_CODES:
            return url, "blocked", f"HTTP {r.status_code}"
        if r.status_code >= 400:
            return url, "broken", f"HTTP {r.status_code}"
        return url, "ok", ""
    except requests.exceptions.Timeout:
        return url, "broken", "timed out"
    except requests.exceptions.RequestException as e:
        return url, "broken", type(e).__name__


def check_links(soup, base_url: str, max_workers: int = 10) -> Result:
    links = collect_links(soup, base_url)
    if not links:
        return Result("Links", "pass", "no links to check")

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        outcomes = list(pool.map(check_one, links))

    broken = [(u, d) for u, kind, d in outcomes if kind == "broken"]
    blocked = [(u, d) for u, kind, d in outcomes if kind == "blocked"]

    if broken:
        details = "; ".join(f"{u} ({d})" for u, d in broken)
        msg = f"{len(broken)} of {len(links)} broken: {details}"
        if blocked:
            msg += f" (+{len(blocked)} could not be verified)"
        return Result("Links", "fail", msg)
    if blocked:
        details = "; ".join(f"{u} ({d})" for u, d in blocked)
        return Result("Links", "warn", f"{len(blocked)} could not be verified: {details}")
    return Result("Links", "pass", f"all {len(links)} links OK")