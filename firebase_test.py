
import firebase_admin
from firebase_admin import firestore

# Connect using local Google Cloud credentials
firebase_admin.initialize_app(
    options={"projectId": "careloop-ai-a79ab"}
)

db = firestore.client()

print("Connecting to CARELOOP AI Firestore...")

try:
    # Fictional test data only
    test_appointment = {
        "doctor": "Dr. Demo",
        "date": "2026-11-20",
        "time": "10:30 AM",
        "location": "Demo Care Clinic",
        "test_record": True
    }

    # Save a document to Firestore
    document_ref = db.collection(
        "connection_tests"
    ).document("demo_appointment")

    document_ref.set(test_appointment)

    print("SUCCESS! Test appointment saved.")

    # Read the saved document
    saved_document = document_ref.get()

    if saved_document.exists:
        print("SUCCESS! Appointment retrieved.")
        print(saved_document.to_dict())
    else:
        print("ERROR: Document was not found.")

except Exception as error:
    print("Firestore test failed.")
    print(f"Error: {error}")
