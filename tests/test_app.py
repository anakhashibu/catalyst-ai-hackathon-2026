
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


def test_care_relay_follow_up(app):
    # Use a fictional medication in the test session.
    app.session_state["medications"] = [
        {
            "id": "test-med-001",
            "name": "Test Medicine",
            "dosage": "1 tablet",
            "time": "09:00",
            "status": "Unconfirmed",
        }
    ]

    # Open the caregiver dashboard.
    app.radio[0].set_value("Caregiver Dashboard").run()

    assert len(app.exception) == 0

    # The caregiver should see a follow-up form.
    follow_up = next(
        item for item in app.selectbox
        if item.label == "Record caregiver follow-up"
    )

    follow_up.set_value("Contacted")

    save_button = next(
        item for item in app.button
        if item.label == "Save follow-up outcome"
    )

    save_button.click().run()

    # Verify the result was stored in session state.
    assert (
        app.session_state["care_relay"]["test-med-001"]
        == "Contacted"
    )

    # Verify the Family Dashboard displays the outcome.
    app.radio[0].set_value("Family Dashboard").run()

    assert len(app.exception) == 0

    
    # Verify the Family Dashboard displays the saved outcome.
    displayed_text = "\n".join(
        str(item.value) for item in app.markdown
    )

    assert "Caregiver follow-up:" in displayed_text
    assert "Contacted" in displayed_text
