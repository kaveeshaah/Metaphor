from bs4 import BeautifulSoup
from seo_lint.checks import check_title, check_meta_description


def make_soup(html):
    return BeautifulSoup(html, "html.parser")


def test_missing_title_fails():
    assert check_title(make_soup("<html></html>")).status == "fail"


def test_good_title_passes():
    html = "<title>A perfectly reasonable page title for SEO</title>"
    assert check_title(make_soup(html)).status == "pass"


def test_missing_meta_description_fails():
    assert check_meta_description(make_soup("<head></head>")).status == "fail"