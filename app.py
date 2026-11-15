
import streamlit as st

st.set_page_config(
    page_title="CARELOOP AI",
    page_icon="💙",
    layout="wide"
)

# Temporary medication storage for this browser session
if "medications" not in st.session_state:
    st.session_state.medications = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

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

    st.header("📅 Upcoming Appointment")
    st.write("Routine check-up — Demo appointment")




# Family dashboard
elif page == "Family Dashboard":
    st.title("👨‍👩‍👧 Family Dashboard")
    st.write("Stay connected with your loved one's care.")

    col1, col2 = st.columns(2)

    col1.metric("Taken Doses", taken_doses)
    col2.metric("Unconfirmed Doses", unconfirmed_doses)

    st.divider()
    st.header("🤝 Care Relay Updates")

    
if unconfirmed_doses > 0:
    st.warning(
        f"{unconfirmed_doses} medication dose(s) "
        "awaiting confirmation."
    )
else:
    st.success("No unconfirmed doses in the current schedule.")

if skipped_doses > 0:
    st.info(
        f"{skipped_doses} dose(s) recorded as skipped."
    )


    st.info(
        "An unconfirmed dose does not necessarily "
        "mean the medication was missed."
    )

# Caregiver dashboard
elif page == "Caregiver Dashboard":
    st.title("🩺 Caregiver Dashboard")
    st.write("Coordinate care and follow-ups.")

    col1, col2 = st.columns(2)

    col1.metric("Demo Patients", 1)
    col2.metric("Unconfirmed Doses", unconfirmed_doses)

    st.divider()
    st.header("📋 Follow-up Queue")

    
    pending_medications = [
        med for med in medications
        if med["status"] == "Unconfirmed"
    ]

    if pending_medications:
        for med in pending_medications:
            st.warning(
                f"Awaiting confirmation: {med['name']} "
                f"— {med['time']}"
        )
    else:
        st.success("No unconfirmed doses to review.")

    st.caption(
        "Unconfirmed doses are shown for review. "
        "Care Relay escalation is not active yet."
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
                st.session_state.medications.append({
                    "id": st.session_state.get("next_med_id", 1),
                    "name": medicine_name.strip(),
                    "dosage": dosage.strip(),
                    "time": medicine_time.strftime("%I:%M %p"),
                    "status": "Unconfirmed"
                })
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
                            medication["status"] = "Taken"
                            st.rerun()

                    with col2:
                        if st.button(
                            "⏭️ Mark as Skipped",
                            key=f"skipped_{medication['id']}"
                        ):
                            medication["status"] = "Skipped"
                            st.rerun()

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
                st.session_state.appointments.append(
                    {
                        "doctor": doctor_name.strip(),
                        "date": appointment_date,
                        "time": appointment_time,
                        "location": location.strip(),
                    }
                )
                st.success("Appointment added successfully!")
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
