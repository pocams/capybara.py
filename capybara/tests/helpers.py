import json
from lxml import etree
from packaging.specifiers import SpecifierSet
from werkzeug.datastructures import ImmutableMultiDict


def extract_results(session):
    session.assert_selector("//pre[@id='results']")

    tree = etree.HTML(session.body)
    element = tree.xpath("//pre[@id='results']")[0]

    def inner_html(elem):
        return "".join(
            [elem.text or ""] +
            [etree.tostring(child).decode("utf-8") for child in elem] +
            [elem.tail or ""])

    return ImmutableMultiDict(json.loads(inner_html(element)))


def isversion(actual, expected):
    if expected is None:
        return True
    if actual is None:
        return False

    return actual in SpecifierSet(expected)


def ismarionette(session, version=None):
    return (
        getattr(session.driver, "_marionette", False) and
        isversion(getattr(session.driver, "_firefox_version", None), browser))


def isselenium(session):
    try:
        from capybara.selenium.driver import Driver
    except ImportError:
        # If we can't import it, then it can't be in use.
        return False

    return isinstance(session.driver, Driver)
