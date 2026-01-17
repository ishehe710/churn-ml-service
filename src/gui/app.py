import streamlit as st
import numpy as np

from src.gui.api_client import predict_churn

st.set_page_config(page_title="Churn Prediction", layout="wide")

st.title("📉 Customer Churn Prediction")
st.write("Enter customer attributes to estimate churn risk.")

with st.form("input_form"):

    # --- Core numeric features ---
    senior_citizen = st.radio("Senior Citizen", ["Yes", "No"], index=1)
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=70.0)
    total_charges = st.number_input("Total Charges", min_value=0.0, max_value=100000.0, value=1000.0)

    # --- Binary one-hot features ---
    binary_features = [
        "female", "male",
        "no_partner", "yes_partner",
        "no_dependents", "yes_dependents",
        "no_phone_service", "yes_phone_service",
        "no_multiple_lines", "no_phone_service_multiple_lines", "yes_multiple_lines",
        "dsl_internet_service", "fiber_optic_internet_service", "no_internet_service",
        "no_online_security", "no_internet_service_online_security", "yes_online_security",
        "no_online_backup", "no_internet_service_online_backup", "yes_online_backup",
        "no_device_protection", "no_internet_service_device_protection", "yes_device_protection",
        "no_tech_support", "no_internet_service_tech_support", "yes_tech_support",
        "no_streaming_tv", "no_internet_service_streaming_tv", "yes_streaming_tv",
        "no_streaming_movies", "no_internet_service_streaming_movies", "yes_streaming_movies",
        "month_to_month_contract", "one_year_contract", "two_year_contract",
        "no_paperless_billing", "yes_paperless_billing",
        "bank_transfer_automatic_payment_method",
        "credit_card_automatic_payment_method",
        "electronic_check_payment_method",
        "mailed_check_payment_method",
    ]

    inputs = {}
    cols = st.columns(3)

    for i, feature in enumerate(binary_features):
        with cols[i % 3]:
            inputs[feature] = st.radio(
                feature.replace("_", " ").title(),
                ["Yes", "No"],
                index=1,
                key=f"radio_{feature}",
            )

    submitted = st.form_submit_button("Predict Churn")

    if submitted:
        try:
            payload = {f: 1 if inputs[f] == "Yes" else 0 for f in binary_features}
            payload["senior_citizen"] = 1 if senior_citizen == "Yes" else 0
            payload["tenure"] = tenure
            payload["monthly_charges"] = monthly_charges
            payload["total_charges"] = total_charges

            response = predict_churn(payload)

            probability = response["probability"]
            label = response["churn_label"]
            model_version = response["model_version"]

            st.success("Prediction successful ✅")

            st.metric(
                label="Churn Probability",
                value=f"{int(np.round(probability * 100))}%",
            )

            st.write(f"**Risk Level:** {'High' if label == 1 else 'Low'}")
            st.write(f"**Model Version:** {model_version}")

        except Exception as e:
            st.error("Prediction failed. Please check the API service.")
            st.exception(e)
