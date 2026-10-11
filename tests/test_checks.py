from bs4 import BeautifulSoup
from seo_lint.checks import (
    check_title,
    check_meta_description,
    check_h1,
    check_image_alts,
    check_canonical,
    check_heading_order,
)


def make_soup(html):
    return BeautifulSoup(html, "html.parser")


# Title checks
def test_missing_title_fails():
    assert check_title(make_soup("<html></html>")).status == "fail"


def test_short_title_warns():
    assert check_title(make_soup("<title>Short</title>")).status == "warn"


def test_good_title_passes():
    html = "<title>A perfectly reasonable page title for SEO</title>"
    assert check_title(make_soup(html)).status == "pass"


# Meta description checks
def test_missing_meta_description_fails():
    assert check_meta_description(make_soup("<head></head>")).status == "fail"


def test_good_meta_description_passes():
    desc = "A" * 140
    html = f'<head><meta name="description" content="{desc}"></head>'
    assert check_meta_description(make_soup(html)).status == "pass"


# H1 checks
def test_missing_h1_fails():
    assert check_h1(make_soup("<body></body>")).status == "fail"


def test_empty_h1_fails():
    assert check_h1(make_soup("<body><h1>   </h1></body>")).status == "fail"


def test_multiple_h1_warns():
    html = "<body><h1>First</h1><h1>Second</h1></body>"
    assert check_h1(make_soup(html)).status == "warn"


def test_single_h1_passes():
    html = "<body><h1>Primary Page Heading</h1></body>"
    assert check_h1(make_soup(html)).status == "pass"


# Image alt checks
def test_no_images_passes():
    assert check_image_alts(make_soup("<body><p>No images</p></body>")).status == "pass"


def test_missing_image_alt_fails():
    html = '<body><img src="pic.jpg"></body>'
    assert check_image_alts(make_soup(html)).status == "fail"


def test_empty_image_alt_fails():
    html = '<body><img src="pic.jpg" alt="  "></body>'
    assert check_image_alts(make_soup(html)).status == "fail"


def test_all_images_have_alt_passes():
    html = '<body><img src="pic.jpg" alt="Description of photo"></body>'
    assert check_image_alts(make_soup(html)).status == "pass"


# Canonical checks
def test_missing_canonical_warns():
    assert check_canonical(make_soup("<head></head>")).status == "warn"


def test_multiple_canonical_fails():
    html = """
    <head>
        <link rel="canonical" href="https://example.com/page1">
        <link rel="canonical" href="https://example.com/page2">
    </head>
    """
    assert check_canonical(make_soup(html)).status == "fail"


def test_empty_canonical_href_fails():
    html = '<head><link rel="canonical" href=""></head>'
    assert check_canonical(make_soup(html)).status == "fail"


def test_good_canonical_passes():
    html = '<head><link rel="canonical" href="https://example.com/page"></head>'
    res = check_canonical(make_soup(html))
    assert res.status == "pass"
    assert res.message == "https://example.com/page"


# Heading order checks
def test_no_headings_fails():
    assert check_heading_order(make_soup("<body><p>Hello</p></body>")).status == "fail"


def test_skipped_heading_order_warns():
    html = "<body><h1>Title</h1><h3>Sub-sub heading</h3></body>"
    res = check_heading_order(make_soup(html))
    assert res.status == "warn"
    assert "skips from h1 to h3" in res.message


def test_valid_heading_order_passes():
    html = """
    <body>
        <h1>Title</h1>
        <h2>Section</h2>
        <h3>Subsection</h3>
        <h2>Another Section</h2>
    </body>
    """
    assert check_heading_order(make_soup(html)).status == "pass"