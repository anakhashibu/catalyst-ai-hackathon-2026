
from care_priority import build_care_priorities


def medication(med_id, status):
    return {
        "id": med_id,
        "name": f"Medicine {med_id}",
        "status": status,
    }


def test_unconfirmed_is_pending():
    result = build_care_priorities(
        [medication("1", "Unconfirmed")], {}
    )
    assert len(result) == 1
    assert result[0]["level"] == "PENDING"


def test_needs_assistance_is_high():
    result = build_care_priorities(
        [medication("1", "Unconfirmed")],
        {"1": "Needs assistance"},
    )
    assert result[0]["level"] == "HIGH"


def test_skipped_requires_review():
    result = build_care_priorities(
        [medication("1", "Skipped")], {}
    )
    assert result[0]["level"] == "REVIEW"


def test_taken_is_not_active():
    result = build_care_priorities(
        [medication("1", "Taken")], {}
    )
    assert result == []


def test_resolved_is_not_active():
    result = build_care_priorities(
        [medication("1", "Unconfirmed")],
        {"1": "Resolved"},
    )
    assert result == []


def test_priority_order():
    meds = [
        medication("1", "Unconfirmed"),
        medication("2", "Skipped"),
        medication("3", "Unconfirmed"),
    ]

    outcomes = {"3": "Needs assistance"}

    result = build_care_priorities(meds, outcomes)

    assert [item["level"] for item in result] == [
        "HIGH",
        "REVIEW",
        "PENDING",
    ]
