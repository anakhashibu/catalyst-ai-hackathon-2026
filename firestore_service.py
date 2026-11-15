
import firebase_admin
from firebase_admin import firestore
from datetime import date, time

PROJECT_ID = "careloop-ai-a79ab"

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_admin.initialize_app(
        options={"projectId": PROJECT_ID}
    )

db = firestore.client()


def save_appointment(appointment):
    """Save one fictional demo appointment."""

    data = {
        "doctor": appointment["doctor"],
        "date": appointment["date"].isoformat(),
        "time": appointment["time"].isoformat(),
        "location": appointment["location"],
        "test_record": True
    }

    document_ref = db.collection(
        "demo_appointments"
    ).document()

    document_ref.set(data)
    return document_ref.id


def load_appointments():
    """Load fictional demo appointments."""

    appointments = []

    documents = db.collection(
        "demo_appointments"
    ).stream()

    for document in documents:
        data = document.to_dict()

        if data.get("test_record") is not True:
            continue

        appointments.append({
            "id": document.id,
            "doctor": data["doctor"],
            "date": date.fromisoformat(data["date"]),
            "time": time.fromisoformat(data["time"]),
            "location": data["location"]
        })

    return appointments
