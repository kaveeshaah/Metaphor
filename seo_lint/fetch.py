import requests

HEADERS = {"User-Agent": "seo-lint/0.1 (learning project)"}


def fetch_page(url: str, timeout: int = 10) -> requests.Response:
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response