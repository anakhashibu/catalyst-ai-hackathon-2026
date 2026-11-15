
import streamlit as st
import os

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
from firestore_service import (
    load_appointments,
    save_appointment,
    load_medications,
    save_medication,
    update_medication_status,
)



st.set_page_config(
    page_title="CARELOOP AI",
    page_icon="💙",
    layout="wide"
)

# Accessibility improvements for elderly users
st.markdown("""
<style>
    /* Larger, readable text */
    html, body, [class*="st-"] {
        font-size: 18px;
    }

    /* Larger buttons and touch targets */
    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 48px;
        font-size: 18px;
        font-weight: 600;
    }

    /* Clear form labels */
    label {
        font-size: 17px !important;
        font-weight: 600 !important;
    }

    /* Improve readability */
    .stMarkdown p {
        line-height: 1.65;
    }

    /* Visible keyboard focus indicator */
    button:focus-visible,
    input:focus-visible {
        outline: 3px solid #2563eb !important;
        outline-offset: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Temporary medication storage for this browser session


# Initialize medications
if "medications" not in st.session_state:
    if DEMO_MODE:
        st.session_state.medications = []
    else:
        try:
            st.session_state.medications = load_medications()
        except Exception as error:
            st.session_state.medications = []
            st.error(f"Could not load demo medications: {error}")


# Initialize appointments
if "appointments" not in st.session_state:
    if DEMO_MODE:
        st.session_state.appointments = []
    else:
        try:
            st.session_state.appointments = load_appointments()
        except Exception as error:
            st.session_state.appointments = []
            st.error(f"Could not load demo appointments: {error}")

# Initialize Care Relay follow-up records
if "care_relay" not in st.session_state:
    st.session_state.care_relay = {}
    
# Shared medication data for all dashboards
medications = st.session_state.medications

total_doses = len(medications)

taken_doses = sum(
    med["status"] == "Taken"
    for med in medications
)

unconfirmed_doses = sum(
    med["status"] == "Unconfirmed"
    for med in medications
)

skipped_doses = sum(
    med["status"] == "Skipped"
    for med in medications
)


# Sidebar navigation
with st.sidebar:
    st.title("💙 CARELOOP AI")
    st.caption("Connected care, every day.")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Home",
            "Elderly Dashboard",
            "Family Dashboard",
            "Caregiver Dashboard",
            "Medication Manager",
            "Appointment Manager",
        ],
    )

    st.divider()
    st.caption("Prototype • Demo data only")

# Home page
if page == "Home":
    st.title("💙 Welcome to CARELOOP AI")
    st.subheader("Intelligent Elderly Care & Medication Management")

    st.write(
        "A connected platform for elderly individuals, "
        "families, and caregivers."
    )

    st.divider()

    st.header("Our Mission")
    st.info(
        "Care doesn't stop at reminders. "
        "It continues until someone knows that the person is okay."
    )

    st.header("Core Features")
    st.write("💊 Medication Management")
    st.write("📅 Appointment Tracking")
    st.write("🤝 Care Relay")
    st.write("👨‍👩‍👧 Family & Caregiver Coordination")
    st.write("🤖 AI Care Assistant — Planned")

# Elderly dashboard
elif page == "Elderly Dashboard":
    st.title("👵 Elderly Dashboard")
    st.write("Your daily care companion.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Scheduled Doses", total_doses)
    col2.metric("Taken", taken_doses)
    col3.metric("Unconfirmed", unconfirmed_doses)

    st.divider()
    
    st.header("💊 Today's Medications")

    if not medications:
        st.info("No medications scheduled yet.")
    else:
        for med in medications:
            message = (
                f"{med['time']} — {med['name']} "
                f"({med['dosage']}) — {med['status']}"
            )

            if med["status"] == "Taken":
                st.success(message)
            elif med["status"] == "Skipped":
                st.error(message)
            else:
                st.warning(message)

    

    st.subheader("📅 Upcoming Appointment")

    from datetime import datetime

    now = datetime.now()

    upcoming_appointments = [
        appointment
        for appointment in st.session_state.appointments
        if datetime.combine(
            appointment["date"],
            appointment["time"]
        ) >= now
    ]

    if upcoming_appointments:
        next_appointment = min(
            upcoming_appointments,
            key=lambda appointment: datetime.combine(
                appointment["date"],
                appointment["time"]
            )
        )

        st.write(f"**Doctor:** {next_appointment['doctor']}")
        st.write(f"**Date:** {next_appointment['date'].strftime('%d %B %Y')}")
        st.write(f"**Time:** {next_appointment['time'].strftime('%I:%M %p')}")
        st.write(f"**Location:** {next_appointment['location']}")
    else:
        st.info("No upcoming appointments scheduled.")







# Family dashboard
elif page == "Family Dashboard":
    st.title("👨‍👩‍👧 Family Dashboard")
    st.write("Stay connected with your loved one's care.")

    # Medication summary
    col1, col2, col3 = st.columns(3)

    col1.metric("Taken Doses", taken_doses)
    col2.metric("Unconfirmed Doses", unconfirmed_doses)
    col3.metric("Skipped Doses", skipped_doses)

    st.divider()

    # Medication updates
    st.header("💊 Medication Updates")

    if unconfirmed_doses > 0:
        st.warning(
            f"{unconfirmed_doses} medication dose(s) "
            "awaiting confirmation."
        )
    else:
        st.success(
            "No unconfirmed doses in the current schedule."
        )

    if skipped_doses > 0:
        st.info(
            f"{skipped_doses} dose(s) recorded as skipped."
        )

    st.info(
        "An unconfirmed dose does not necessarily "
        "mean the medication was missed."
    )

    st.divider()

    # Care Relay follow-up information
    st.header("🤝 Care Relay Follow-ups")

    if not st.session_state.care_relay:
        st.info("No caregiver follow-ups recorded yet.")

    else:
        follow_up_count = 0

        for med in medications:
            med_id = str(med["id"])

            if med_id in st.session_state.care_relay:
                follow_up_count += 1

                outcome = st.session_state.care_relay[med_id]

                with st.container(border=True):
                    st.subheader(med["name"])

                    st.write(
                        f"**Medication status:** {med['status']}"
                    )

                    st.write(
                        f"**Caregiver follow-up:** {outcome}"
                    )

                    if outcome == "Needs assistance":
                        st.warning(
                            "Caregiver recorded that assistance "
                            "may be required."
                        )

                    elif outcome == "Resolved":
                        st.success(
                            "Caregiver marked the follow-up as resolved."
                        )

                    elif outcome == "Contacted":
                        st.info(
                            "Caregiver recorded that contact was made."
                        )

        if follow_up_count == 0:
            st.info(
                "No follow-up records match the current medications."
            )

    st.caption(
        "Care Relay is a manual demonstration workflow. "
        "Follow-up outcomes do not confirm medication intake."
    )



# Caregiver dashboard
elif page == "Caregiver Dashboard":
    st.title("🩺 Caregiver Dashboard")
    st.write("Coordinate care and follow-ups.")

    pending_medications = [
        med for med in medications
        if med["status"] == "Unconfirmed"
    ]

    col1, col2 = st.columns(2)
    col1.metric("Demo Patients", 1)
    col2.metric("Unconfirmed Doses", len(pending_medications))

    st.divider()
    st.header("🤝 Care Relay — Follow-up Queue")

    st.info(
        "Care Relay allows caregivers to record follow-up "
        "outcomes for medication doses awaiting confirmation. "
        "This is a manual demonstration workflow."
    )

    if not pending_medications:
        st.success("No unconfirmed doses to review.")

    for med in pending_medications:
        med_id = str(med["id"])

        with st.container(border=True):
            st.subheader(med["name"])
            st.write(f"Scheduled time: {med['time']}")
            st.write(f"Dosage: {med['dosage']}")
            st.warning("Medication confirmation pending")

            existing_outcome = st.session_state.care_relay.get(
                med_id, "Not contacted"
            )

            st.write(f"**Follow-up status:** {existing_outcome}")

            with st.form(f"relay_form_{med_id}"):
                outcome = st.selectbox(
                    "Record caregiver follow-up",
                    [
                        "Not contacted",
                        "Contacted",
                        "Needs assistance",
                        "Resolved"
                    ],
                    index=[
                        "Not contacted",
                        "Contacted",
                        "Needs assistance",
                        "Resolved"
                    ].index(existing_outcome),
                    key=f"relay_outcome_{med_id}"
                )

                submitted = st.form_submit_button(
                    "Save follow-up outcome"
                )

                if submitted:
                    st.session_state.care_relay[med_id] = outcome
                    st.success("Follow-up outcome recorded.")
                    st.rerun()

    st.caption(
        "An unconfirmed dose is not necessarily missed. "
        "Care Relay does not confirm medication intake "
        "or send automatic notifications in this prototype."
    )





# Medication Manager
elif page == "Medication Manager":
    st.title("💊 Medication Manager")
    st.write("Manage medication schedules and dose confirmations.")

    st.header("➕ Add Medication")

    with st.form("medication_form", clear_on_submit=True):
        medicine_name = st.text_input("Medication Name")
        dosage = st.text_input(
            "Prescribed Dosage",
            placeholder="Example: 1 tablet"
        )
        medicine_time = st.time_input("Scheduled Time")

        submitted = st.form_submit_button("Add Medication")

        
        if submitted:
            if medicine_name.strip() and dosage.strip():

                new_medication = {
                    "name": medicine_name.strip(),
                    "dosage": dosage.strip(),
                    "time": medicine_time,
                    "status": "Unconfirmed"
                }

                
                try:
                    if DEMO_MODE:
                        new_medication["id"] = f"demo_{len(st.session_state.medications) + 1}"
                        st.session_state.medications.append(new_medication)
                        st.success("Medication added to your demo schedule!")
                    else:
                        save_medication(new_medication)
                        st.session_state.medications = load_medications()
                        st.success("Medication saved permanently!")

                except Exception as error:
                    st.error(f"Could not save medication: {error}")
 
            else:
                st.warning(
                    "Please enter the medication name and dosage."
                )

                st.session_state.next_med_id = (
                    st.session_state.get("next_med_id", 1) + 1
                )
                st.success("Medication added successfully!")
        else:
            st.error("Please enter the medication name and dosage.")

    st.divider()
    st.header("📋 Medication Schedule")

    if not st.session_state.medications:
        st.info("No medications added yet.")
    else:
        for medication in st.session_state.medications:
            with st.container(border=True):
                st.subheader(medication["name"])
                st.write(f"Dosage: {medication['dosage']}")
                st.write(f"Time: {medication['time']}")
                st.write(f"Status: **{medication['status']}**")

                
            if medication["status"] == "Unconfirmed":
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "✅ Mark as Taken",
                        key=f"taken_{medication['id']}"
                    ):
                        
                        try:
                            if DEMO_MODE:
                                medication["status"] = "Taken"
                            else:
                                update_medication_status(medication["id"], "Taken")
                                st.session_state.medications = load_medications()

                            st.rerun()

                        except Exception as error:
                            st.error(f"Could not update medication: {error}")

                with col2:
                    if st.button(
                        "⏭️ Mark as Skipped",
                        key=f"skipped_{medication['id']}"
                    ):
                        try:
                            if DEMO_MODE:
                                medication["status"] = "Skipped"
                            else:
                                update_medication_status(
                                    medication["id"], "Skipped"
                                )
                                st.session_state.medications = load_medications()

                            st.rerun()

                        except Exception as error:
                            st.error(f"Could not update medication: {error}")

            
            else:
                st.success(
                    f"Dose recorded as {medication['status']}."
                )


    st.caption(
        "Demo only. Medication entries must follow "
        "instructions from a qualified healthcare professional."
    )

    st.caption("CARELOOP AI | Hackathon Prototype | Demo data only")

# Appointment Manager
elif page == "Appointment Manager":
    st.title("📅 Appointment Manager")
    st.write("Manage upcoming medical appointments.")

    st.header("➕ Add Appointment")

    with st.form("appointment_form", clear_on_submit=True):
        doctor_name = st.text_input("Doctor's Name")
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        location = st.text_input("Hospital / Clinic")

        submitted = st.form_submit_button("Add Appointment")

        
        if submitted:
            if doctor_name.strip() and location.strip():

                new_appointment = {
                    "doctor": doctor_name.strip(),
                    "date": appointment_date,
                    "time": appointment_time,
                    "location": location.strip()
                }

                
                try:
                    if DEMO_MODE:
                        # Store only in the current demo session
                        st.session_state.appointments.append(
                            new_appointment
                        )

                        st.success(
                            "Demo appointment added successfully!"
                        )

                    else:
                        # Save permanently in Firestore
                        appointment_id = save_appointment(
                            new_appointment
                        )

                        st.session_state.appointments = (
                            load_appointments()
                        )

                        st.success(
                            "Appointment saved permanently!"
                        )

                except Exception as error:
                    st.error(
                        f"Could not save appointment: {error}"
                    )


            else:
                st.warning(
                    "Please enter the doctor's name and hospital."
                )


    st.divider()
    st.header("📋 Scheduled Appointments")

    if not st.session_state.appointments:
        st.info("No appointments scheduled yet.")
    else:
        for appointment in st.session_state.appointments:
            with st.container(border=True):
                st.subheader(appointment["doctor"])
                st.write(f"Date: {appointment['date']}")
                st.write(
                    f"Time: {appointment['time'].strftime('%I:%M %p')}"
                )
                st.write(f"Location: {appointment['location']}")
