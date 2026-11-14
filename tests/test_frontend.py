
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_PATH = PROJECT_ROOT / "frontend"
FRONTEND_URL = "http://127.0.0.1:5500"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


@pytest.fixture(scope="module")
def frontend_server():
    import os

    previous_directory = os.getcwd()
    os.chdir(FRONTEND_PATH)

    server = ThreadingHTTPServer(
        ("127.0.0.1", 5500),
        QuietHandler
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True
    )
    thread.start()

    time.sleep(0.5)

    yield

    server.shutdown()
    server.server_close()
    os.chdir(previous_directory)


@pytest.fixture
def browser_page(frontend_server):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(FRONTEND_URL)
        page.wait_for_load_state("domcontentloaded")

        yield page

        browser.close()


def test_frontend_loads(browser_page):
    assert browser_page.title() != ""


def test_search_input_visible(browser_page):
    assert browser_page.locator("#searchInput").is_visible()
    assert browser_page.locator("#searchButton").is_visible()


def test_search_button_exists(browser_page):
    assert browser_page.locator("#searchButton").count() == 1


def test_filter_controls_visible(browser_page):
    assert browser_page.locator("#genreFilter").is_visible()
    assert browser_page.locator("#ratingFilter").is_visible()
    assert browser_page.locator("#clearFilters").is_visible()


def test_search_history_section_visible(browser_page):
    assert browser_page.locator("#historyList").count() == 1
    assert browser_page.locator("#refreshHistory").is_visible()
    assert browser_page.locator("#clearHistory").is_visible()


def test_movie_modal_exists(browser_page):
    assert browser_page.locator("#movieModal").count() == 1
    assert browser_page.locator("#closeModal").count() == 1


def test_search_interstellar(browser_page):
    browser_page.locator("#searchInput").fill("Interstellar")
    browser_page.locator("#searchButton").click()

    browser_page.locator("#results").get_by_text(
        "Interstellar",
        exact=True
    ).wait_for(timeout=10000)

    assert "Interstellar" in browser_page.locator("#results").inner_text()


def test_search_inception(browser_page):
    browser_page.locator("#searchInput").fill("Inception")
    browser_page.locator("#searchButton").click()

    browser_page.locator("#results").get_by_text(
        "Inception",
        exact=False
    ).wait_for(timeout=10000)

    assert "Inception" in browser_page.locator("#results").inner_text()


def test_autocomplete(browser_page):
    browser_page.locator("#searchInput").fill("In")

    browser_page.locator("#suggestions li").first.wait_for(
        state="visible",
        timeout=10000
    )

    assert browser_page.locator("#suggestions li").count() > 0


def test_movie_details_popup(browser_page):
    browser_page.locator("#searchInput").fill("Interstellar")
    browser_page.locator("#searchButton").click()

    movie_card = browser_page.locator("#results").get_by_text(
        "Interstellar",
        exact=False
    ).first

    movie_card.wait_for(timeout=10000)
    movie_card.click()

    browser_page.locator("#movieModal").wait_for(
        state="visible",
        timeout=10000
    )

    assert browser_page.locator("#movieDetails").inner_text() != ""


def test_close_movie_popup(browser_page):
    browser_page.locator("#searchInput").fill("Interstellar")
    browser_page.locator("#searchButton").click()

    movie_card = browser_page.locator("#results").get_by_text(
        "Interstellar",
        exact=False
    ).first

    movie_card.wait_for(timeout=10000)
    movie_card.click()

    browser_page.locator("#movieModal").wait_for(state="visible")
    browser_page.locator("#closeModal").click()

    assert browser_page.locator("#movieModal").is_hidden()
