from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class Result:
    name: str
    status: str   # "pass", "warn", or "fail"
    message: str


def check_title(soup: BeautifulSoup) -> Result:
    tag = soup.find("title")
    title = tag.get_text(strip=True) if tag else ""

    if not title:
        return Result("Title tag", "fail", "missing or empty")

    length = len(title)
    if length < 30:
        return Result("Title tag", "warn", f"too short ({length} chars, aim for 30-60)")
    if length > 60:
        return Result("Title tag", "warn", f"too long ({length} chars, aim for 30-60)")
    return Result("Title tag", "pass", f"present ({length} chars)")


def check_meta_description(soup: BeautifulSoup) -> Result:
    tag = soup.find("meta", attrs={"name": "description"})
    content = tag.get("content", "").strip() if tag else ""

    if not content:
        return Result("Meta description", "fail", "missing or empty")

    length = len(content)
    if length < 120:
        return Result("Meta description", "warn", f"too short ({length} chars, aim for 120-160)")
    if length > 160:
        return Result("Meta description", "warn", f"too long ({length} chars, aim for 120-160)")
    return Result("Meta description", "pass", f"present ({length} chars)")


ALL_CHECKS = [check_title, check_meta_description]