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


def check_h1(soup: BeautifulSoup) -> Result:
    h1s = soup.find_all("h1")
    count = len(h1s)

    if count == 0:
        return Result("H1 tag", "fail", "missing")
    if count > 1:
        return Result("H1 tag", "warn", f"{count} found (aim for exactly 1)")
    text = h1s[0].get_text(strip=True)
    if not text:
        return Result("H1 tag", "fail", "empty")
    return Result("H1 tag", "pass", f"present ({len(text)} chars)")


def check_image_alts(soup: BeautifulSoup) -> Result:
    images = soup.find_all("img")
    if not images:
        return Result("Image alt text", "pass", "no images found")

    missing = [img for img in images if not (img.get("alt") or "").strip()]
    if missing:
        return Result(
            "Image alt text", "fail",
            f"{len(missing)} of {len(images)} images missing alt text",
        )
    return Result("Image alt text", "pass", f"all {len(images)} images have alt text")


ALL_CHECKS = [
    check_title,
    check_meta_description,
    check_h1,
    check_image_alts,
]