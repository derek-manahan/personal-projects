import streamlit as st

# Title and subtitle
st.markdown(
    "<h1 style='color:#bfdb64;'>Student Technology Equity Program (STEP) Eligibility Checker</h1>",
    unsafe_allow_html=True
)
st.markdown("**Note:** This tool is 100% confidential. No information will be saved. <u>**Eligibility through this tool will not guarantee assistance by STEP.**</u>", unsafe_allow_html=True)

# Initialized for later check that all required options are filled out
inputs_valid = False

# Calculated "Need Factor," which is used to assess student eligibility
NF = 0

# Checking student enrollment status
undergrad_status = st.radio("Are you a UC Berkeley enrolled undergraduate student?", ["Yes", "No"], index=None)
if undergrad_status == "Yes":
    student_type = "Undergraduate"
elif undergrad_status == "No":
    grad_status = st.radio("Are you a UC Berkeley enrolled graduate student?", ["Yes", "No"], index=None)
    if grad_status == "Yes":
        student_type = "Graduate"
    elif grad_status == "No":
        st.error("⚠️ Visiting scholars are ineligible for STEP assistance as our program is funded through the Instructional Resilience & Enhancement Fee (IREF), paid through enrolled student tuition.")
        st.stop()

# Checking student instruction status
instructor_status = st.radio("Are you currently a graduate/undergraduate student instructor (GSI/UGSI)?", ["Yes", "No"], index=None)
if instructor_status == "Yes":
    NF += 1.5

# Checking student financial support
aid_check = st.radio("Did you submit a FAFSA application for the current academic year (or semester you are applying for)?", ["Yes", "No"], index=None)
if aid_check == "Yes":
    SAI = st.number_input("Enter your FAFSA Student Aid Index (SAI): | **CalCentral > My Finances > Financial Aid & Scholarships Profile**", step=1, format="%d", placeholder="Enter your SAI")
    if SAI <= 0.0:
        NF += 3
    elif 1.0 <= SAI <= 750:
        NF += 2
    elif 751 <= SAI <= 6655:
        NF += 1
    else:
        NF += 0

# Checking if student submitted CADAA instead of FAFSA
elif aid_check == "No":
    cadaa_check = st.radio("Did you submit a CA Dream Act (CADAA) application for the current academic year (or semester you are applying for)?", ["Yes", "No"], index=None)
    if cadaa_check == "Yes":
            NF += 3

# Checks that all needed options are filled to display button
inputs_valid = (
    undergrad_status is not None and
    (undergrad_status != "No" or grad_status is not None) and
    instructor_status is not None and
    aid_check is not None and
    (aid_check != "No" or ('cadaa_check' in locals() and cadaa_check is not None))
)

# If all necessary info is given, check eligibility
if inputs_valid:
    if st.button("Check Eligibility"):
        st.markdown("---")

# Highest need factor means student is eligible for all tech
        if NF >= 3.0:
            st.success("✅ You are likely **eligible for ALL technology** offered by STEP.")
            st.success(
                "📶 If you live off campus (within Berkeley, or elsewhere in the United States or Puerto Rico), you are eligible for a **Wi-Fi hotspot**. **University affiliated housing is ineligible for hotspot assistance.**")
            st.info(
                "Please note that student device loan approvals are dependent on **technology availability**. Visit: **https://studenttech.berkeley.edu/step-hardware-offerings**")

# Need factor from 1.0-3.0 means student is eligible for some tech
        elif 3.0 > NF >= 1.0:
            if student_type == "Graduate":
                st.warning(
                    "⚠️ For graduate students who do not receive financial aid, your eligibility for **laptops and hotspots** will be manually reviewed based on additional verification questions.")
            else:
                st.warning("⚠️ You are likely **ineligible** for laptops and hotspots.")
            st.write("**You are likely eligible for the following technology offered by STEP:**")
            permitted = [
                "Microphone", "Wacom Drawing Tablet", "USB Headphones", "iClicker", "Bluetooth Keyboard",
                "Bluetooth Mouse", "Graphing Calculator", "Belkin adapter", "Apple adapter",
                "USB webcam", "Wi-Fi Adapter", "YubiKey"
            ]
            for device in permitted:
                st.write(f"• {device}")
            st.info(
                "Please note that student device loan approvals are dependent on **technology availability**. Visit: **https://studenttech.berkeley.edu/step-hardware-offerings**")

# Grad students with no aid have a different app review process
        else:
            if student_type == "Graduate":
                st.error("Unfortunately, we cannot measure your eligibility through this tool.")
                st.write("For graduate students who do not receive financial aid, your application will be manually reviewed based on additional verification questions.")

# Need factor below 1.0 means student is ineligible for assistance
            else:
                st.error("Unfortunately, your financial need likely falls outside of STEP's eligibility.")
                st.info(
                    "Please note that student device loan approvals are dependent on **technology availability**. Visit: **https://studenttech.berkeley.edu/step-hardware-offerings**")
