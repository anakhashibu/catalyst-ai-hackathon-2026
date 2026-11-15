
"""Explainable, non-clinical care follow-up prioritization."""


def build_care_priorities(medications, care_relay):
    priorities = []

    for med in medications:
        med_id = str(med.get("id", ""))
        name = str(med.get("name", "Medication"))
        status = med.get("status", "Unconfirmed")
        outcome = care_relay.get(med_id, "Not contacted")

        if outcome == "Needs assistance":
            priority = 1
            level = "HIGH"
            message = (
                "A caregiver recorded that assistance may "
                "be needed. Review this follow-up."
            )

        elif outcome == "Resolved":
            continue

        elif status == "Skipped":
            priority = 2
            level = "REVIEW"
            message = (
                "This dose was marked skipped. Review "
                "the recorded status without assuming why."
            )

        elif status == "Unconfirmed":
            priority = 3
            level = "PENDING"
            message = (
                "Dose confirmation is pending. This does "
                "not mean the medication was missed."
            )

        else:
            continue

        priorities.append({
            "medication_id": med_id,
            "name": name,
            "medication_status": status,
            "follow_up": outcome,
            "priority": priority,
            "level": level,
            "message": message,
        })

    return sorted(
        priorities,
        key=lambda item: (item["priority"], item["name"])
    )
