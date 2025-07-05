import streamlit as st

st.title("STEP Eligibility Checker")
st.markdown("**Note:** This tool is 100% confidential. No information will be saved. <u>**Eligibility through this tool will not guarantee assistance by STEP.**</u>", unsafe_allow_html=True)

NF = 0

undergrad_status = st.radio("Are you an enrolled undergraduate student?", ["Yes", "No"])
if undergrad_status == "Yes":
    student_type = "Undergraduate"
else:
    grad_status = st.radio("Are you an enrolled graduate student?", ["Yes", "No"])
    if grad_status == "Yes":
        student_type = "Graduate"
    else:
        st.error("Visiting scholars are ineligible for STEP assistance as our program is funded through the Instructional Resilience & Enhancement Fee (IREF).")
        st.stop()

instructor_status = st.radio("Are you currently a graduate/undergraduate student instructor (GSI/UGSI)?", ["Yes", "No"])
if instructor_status == "Yes":
    NF += 1.5

aid_check = st.radio("Did you submit a FAFSA application for the current school year?", ["Yes", "No"])
if aid_check == "Yes":
    SAI = st.number_input("Enter your FAFSA Student Aid Index (SAI): | **CalCentral > My Finances > Financial Aid & Scholarships Profile**")
    if SAI <= 0.0:
        NF += 3
    elif 1.0 <= SAI <= 750:
        NF += 2
    elif 751 <= SAI <= 6655:
        NF += 1
    else:
        NF += 0
else:
    cadaa_check = st.radio("Did you submit a CA Dream Act (CADAA) application for the current school year?", ["Yes", "No"])
    if cadaa_check == "Yes":
            NF += 3

if st.button("Check Eligibility"):
    st.markdown("---")
    if NF >= 3.0:
        st.success("✅ You are likely **eligible for ALL technology** offered by STEP.")
        st.success(
            "📶 If you live off campus (within Berkeley, or elsewhere in the United States or Puerto Rico), you are eligible for a **Wi-Fi hotspot**. **University affiliated housing is ineligible for hotspot assistance.**")
        st.info(
            "Please note that student device loan approvals are dependent on **technology availability**. Visit: **https://studenttech.berkeley.edu/step-hardware-offerings**")
    elif 3.0 > NF >= 1.0:
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
    else:
        if student_type == "Graduate":
            st.error("Unfortunately, we cannot measure your eligibility through this tool.")
            st.write("For graduate students who do not receive financial aid, your application will be manually reviewed based on additional verification questions.")
        else:
            st.error("Unfortunately, your financial need likely falls outside of STEP's eligibility.")
            st.info(
                "Please note that student device loan approvals are dependent on **technology availability**. Visit: **https://studenttech.berkeley.edu/step-hardware-offerings**")