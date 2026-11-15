
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


# Locate app.py in the main project folder
APP_PATH = Path(__file__).resolve().parent.parent / "app.py"


@pytest.fixture
def app(monkeypatch):
    # Always use demo mode during testing
    monkeypatch.setenv("DEMO_MODE", "true")

    test_app = AppTest.from_file(
        APP_PATH,
        default_timeout=15
    )

    test_app.run()

    assert len(test_app.exception) == 0

    return test_app


def test_home_page_loads(app):
    assert any(
        "CARELOOP AI" in title.value
        for title in app.title
    )


@pytest.mark.parametrize("page", [
    "Elderly Dashboard",
    "Family Dashboard",
    "Caregiver Dashboard",
    "Medication Manager",
    "Appointment Manager",
])
def test_navigation_pages_load(app, page):
    app.radio[0].set_value(page).run()

    assert len(app.exception) == 0

    assert any(
        page in title.value
        for title in app.title
    )
