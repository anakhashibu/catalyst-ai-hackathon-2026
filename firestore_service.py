
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



def save_medication(medication):
    """Save a fictional medication to Firestore."""

    data = {
        "name": medication["name"],
        "dosage": medication["dosage"],
        "time": medication["time"].isoformat(),
        "status": "Unconfirmed",
        "test_record": True
    }

    document_ref = db.collection(
        "demo_medications"
    ).document()

    document_ref.set(data)

    return document_ref.id


def load_medications():
    """Load fictional medications from Firestore."""

    medications = []

    documents = db.collection(
        "demo_medications"
    ).stream()

    for document in documents:
        data = document.to_dict()

        if data.get("test_record") is not True:
            continue

        medications.append({
            "id": document.id,
            "name": data["name"],
            "dosage": data["dosage"],
            "time": time.fromisoformat(data["time"]),
            "status": data["status"]
        })

    return medications


def update_medication_status(medication_id, new_status):
    """Update the confirmation status of a medication."""

    allowed_statuses = ["Unconfirmed", "Taken", "Skipped"]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid medication status")

    db.collection(
        "demo_medications"
    ).document(medication_id).update({
        "status": new_status
    })
