
# CARELOOP AI
### Connected Elderly Care & Medication Management Prototype

CARELOOP AI is a Streamlit-based healthcare coordination prototype built for the CATALYST Solo AI Hackathon.

It explores how older adults, family members, and caregivers can coordinate medication adherence, appointments, and caregiver follow-ups through a simple, accessible interface.

> **Project status:** Working hackathon prototype. Not a production medical system.

## Live Demo

https://careloop-ai-nfxv.onrender.com

## The Problem

Older adults may manage multiple medications and appointments. Family members and caregivers often lack a simple, shared view of medication confirmations and follow-up needs.

CARELOOP AI explores a coordinated workflow designed to improve visibility while supporting the older adult's independence.

## Implemented Features

### 1. Elderly Dashboard
- Medication adherence overview
- Taken, skipped, and unconfirmed medication status visibility
- Simple dashboard interface

### 2. Medication Manager
- Add medication schedules
- View medication details
- Record medications as Taken or Skipped
- Track Unconfirmed doses

### 3. Appointment Manager
- Add doctor appointments
- View saved appointment details

### 4. Family Dashboard
- View medication status summaries
- Identify unconfirmed and skipped doses
- Review caregiver follow-up outcomes

### 5. Caregiver Dashboard and Care Relay
- View medications awaiting confirmation
- Record a manual follow-up outcome:
  - Not contacted
  - Contacted
  - Needs assistance
  - Resolved
- Display recorded follow-ups on the Family Dashboard


### 6. Smart Care Priority Engine

CARELOOP AI includes an explainable, rule-based
care prioritization engine.

The engine:
- Highlights caregiver follow-ups marked Needs assistance
- Identifies skipped medication doses for review
- Tracks doses awaiting confirmation
- Excludes completed and resolved items from active priorities
- Displays explanations for each priority level

The engine supports non-clinical care coordination.
It does not use a trained AI model, diagnose conditions,
or provide medical recommendations.

Six automated tests verify its prioritization logic.

Care Relay is currently a manual coordination workflow. It does not automatically contact caregivers or send notifications.

## Technology Stack

| Layer | Technology |
|---|---|
| User interface | Streamlit |
| Programming language | Python |
| Development database | Firebase Cloud Firestore |
| Public demo data | Streamlit session state |
| Containerization | Docker |
| Hosting | Render |
| Version control | Git and GitHub |
| Automated testing | pytest and Streamlit AppTest |

## How to Try the Demo

1. Open the live application.
2. Navigate to Medication Manager.
3. Add a fictional medication and leave it Unconfirmed.
4. Open Caregiver Dashboard.
5. Select a follow-up outcome such as Contacted.
6. Save the outcome.
7. Open Family Dashboard and review the Care Relay update.
8. Return to Medication Manager and mark the medication Taken or Skipped.

The public demo uses temporary session-based data. It is not intended for real patient records.

## Run Locally

### Prerequisites
- Python
- pip

### Setup

Clone the repository:

```bash
git clone https://github.com/anakhashibu/catalyst-ai-hackathon-2026.git
cd catalyst-ai-hackathon-2026
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch in demo mode:

```bash
DEMO_MODE=true python -m streamlit run app.py
```

For local Firestore development, Google Cloud Application Default Credentials and a correctly configured Firebase project are required. The public demo does not require Firestore credentials.

## Automated Tests

The project includes automated tests for:

- Medication status values
- Date and time serialization
- Home page loading
- Dashboard navigation
- Caregiver follow-up submission
- Family Dashboard follow-up visibility

Run the tests:

```bash
python -m pip install pytest
DEMO_MODE=true python -m pytest tests/ -v
```

**Latest locally reported test result:** 10 passed.

## Architecture

The Streamlit application provides dashboard navigation and user interactions.

In public demo mode:
- Records are held in Streamlit session state.
- Medication status changes update the current session.
- Care Relay follow-ups are available within the same session.
- The application does not connect to Firestore.

In local development mode:
- The Firestore service supports storing and retrieving medication and appointment records.
- Care Relay follow-up state is currently session-based.

## Accessibility Considerations

The prototype includes:
- Larger interactive controls
- Readable labels and text
- Visible medication status information
- Simplified navigation

Formal accessibility and assistive-technology testing has not yet been completed.

## Current Limitations

- The public demo does not provide secure, passcode-based role authentication.
- Different browser sessions do not share the same Care Relay records.
- Automated email reminders are not implemented.
- AI-driven clinical or medication recommendations are not implemented.
- Care Relay does not automatically detect or escalate missed doses.
- Session-based demo records are temporary.
- The prototype is not suitable for real clinical use.

An **Unconfirmed** medication dose must not be treated as proof that the dose was missed.

## Future Development

- Secure passcode-based access with role authorization
- Persistent shared care records for multiple authorized users
- Scheduled email reminders and escalation workflows
- Medication and appointment notification scheduling
- Accessible AI assistance for non-clinical care coordination
- Broader automated testing and accessibility evaluation

## Responsible Use

CARELOOP AI is an educational prototype.

Do not enter real patient information or rely on the application for medication decisions, emergencies, or clinical advice.

## Hackathon

**Event:** CATALYST – Solo AI Hackathon  
**Challenge:** Elderly Care & Medication Management Platform  
**Developer:** Anakha Shibu
