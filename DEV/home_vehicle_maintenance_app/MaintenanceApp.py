import streamlit as st
from datetime import date


def main():
    st.set_page_config(page_title="Home Vehicle Maintenance Claims", layout="centered")
    st.title("Home Vehicle Maintenance Claims")
    st.write("Track and submit maintenance claims for your home and vehicle services.")

    claim_type = st.selectbox("Claim type", ["Home", "Vehicle"])
    description = st.text_area("Issue description")
    cost_estimate = st.number_input("Estimated cost ($)", min_value=0.0, step=0.01, format="%.2f")
    service_date = st.date_input("Date of service", value=date.today())

    if st.button("Submit claim"):
        if not description.strip():
            st.error("Please provide a description for the claim.")
            return

        st.success("Claim submitted successfully.")
        st.markdown("**Claim details**")
        st.write({
            "Claim type": claim_type,
            "Description": description,
            "Estimated cost": f"${cost_estimate:.2f}",
            "Date of service": service_date.isoformat(),
        })


if __name__ == "__main__":
    main()
