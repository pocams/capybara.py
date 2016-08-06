import pytest


class TestHasCSS:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_selector_is_on_the_page(self, session):
        assert session.has_css("p")
        assert session.has_css("p a#foo")

    def test_is_false_if_the_given_selector_is_not_on_the_page(self, session):
        assert not session.has_css("abbr")
        assert not session.has_css("p a#doesnotexist")
        assert not session.has_css("p.nosuchclass")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert session.has_css("a#foo")
            assert not session.has_css("a#red")

    def test_waits_for_content_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_css("input[type='submit'][value='New Here']")