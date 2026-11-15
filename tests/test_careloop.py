
from datetime import date, time


def test_medication_status_values():
    allowed_statuses = {
        "Unconfirmed",
        "Taken",
        "Skipped"
    }

    assert "Taken" in allowed_statuses
    assert "Skipped" in allowed_statuses
    assert "Unconfirmed" in allowed_statuses
    assert "Invalid" not in allowed_statuses


def test_appointment_date_conversion():
    appointment_date = date(2026, 11, 20)

    stored_date = appointment_date.isoformat()
    restored_date = date.fromisoformat(stored_date)

    assert restored_date == appointment_date


def test_medication_time_conversion():
    scheduled_time = time(10, 30)

    stored_time = scheduled_time.isoformat()
    restored_time = time.fromisoformat(stored_time)

    assert restored_time == scheduled_time
