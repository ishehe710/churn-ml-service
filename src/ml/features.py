"""
features.py

Owns:
- Numeric scaling
- Categorical encoding
- Feature normalization

Does NOT:
- Load models
- Perform predictions
- Know about FastAPI
- Have preprocessing logic
"""

from src.api.schema import ChurnInput
import pandas as pd

# model features
FEATURES = [
  "SeniorCitizen",
  "tenure",
  "MonthlyCharges",
  "TotalCharges",
  "Female (gender)",
  "Male (gender)",
  "No (Partner)",
  "Yes (Partner)",
  "No (Dependents)",
  "Yes (Dependents)",
  "No (PhoneService)",
  "Yes (PhoneService)",
  "No (MultipleLines)",
  "No phone service (MultipleLines)",
  "Yes (MultipleLines)",
  "DSL (InternetService)",
  "Fiber optic (InternetService)",
  "No (InternetService)",
  "No (OnlineSecurity)",
  "No internet service (OnlineSecurity)",
  "Yes (OnlineSecurity)",
  "No (OnlineBackup)",
  "No internet service (OnlineBackup)",
  "Yes (OnlineBackup)",
  "No (DeviceProtection)",
  "No internet service (DeviceProtection)",
  "Yes (DeviceProtection)",
  "No (TechSupport)",
  "No internet service (TechSupport)",
  "Yes (TechSupport)",
  "No (StreamingTV)",
  "No internet service (StreamingTV)",
  "Yes (StreamingTV)",
  "No (StreamingMovies)",
  "No internet service (StreamingMovies)",
  "Yes (StreamingMovies)",
  "Month-to-month (Contract)",
  "One year (Contract)",
  "Two year (Contract)",
  "No (PaperlessBilling)",
  "Yes (PaperlessBilling)",
  "Bank transfer (automatic) (PaymentMethod)",
  "Credit card (automatic) (PaymentMethod)",
  "Electronic check (PaymentMethod)",
  "Mailed check (PaymentMethod)"
]

# this function takes ChurnInput schema and converts it into dataframe for the model to use.
def map_churn_input_to_df(data: ChurnInput):
  return pd.DataFrame([{
    "SeniorCitizen": data.senior_citizen,
    "tenure": data.tenure,
    "MonthlyCharges": data.monthly_charges,
    "TotalCharges": data.total_charges,
    "Female (gender)": int(data.female),
    "Male (gender)": int(data.male),
    "No (Partner)": int(data.no_partner),
    "Yes (Partner)": int(data.yes_partner),
    "No (Dependents)": int(data.no_dependents),
    "Yes (Dependents)": int(data.yes_dependents),
    "No (PhoneService)": int(data.no_phone_service),
    "Yes (PhoneService)": int(data.yes_phone_service),
    "No (MultipleLines)": int(data.no_multiple_lines),
    "No phone service (MultipleLines)": int(data.no_phone_service_multiple_lines),
    "Yes (MultipleLines)": int(data.yes_multiple_lines),
    "DSL (InternetService)": int(data.dsl_internet_service),
    "Fiber optic (InternetService)": int(data.fiber_optic_internet_service),
    "No (InternetService)": int(data.no_internet_service),
    "No (OnlineSecurity)": int(data.no_online_security),
    "No internet service (OnlineSecurity)": int(data.no_internet_service_online_security),
    "Yes (OnlineSecurity)": int(data.yes_online_security),
    "No (OnlineBackup)": int(data.no_online_backup),
    "No internet service (OnlineBackup)": int(data.no_internet_service_online_backup),
    "Yes (OnlineBackup)": int(data.yes_online_backup),
    "No (DeviceProtection)": int(data.no_device_protection),
    "No internet service (DeviceProtection)": int(data.no_internet_service_device_protection),
    "Yes (DeviceProtection)": int(data.yes_device_protection),
    "No (TechSupport)": int(data.no_tech_support),
    "No internet service (TechSupport)": int(data.no_internet_service_tech_support),
    "Yes (TechSupport)": int(data.yes_tech_support),
    "No (StreamingTV)": int(data.no_streaming_tv),
    "No internet service (StreamingTV)": int(data.no_internet_service_streaming_tv),
    "Yes (StreamingTV)": int(data.yes_streaming_tv),
    "No (StreamingMovies)": int(data.no_streaming_movies),
    "No internet service (StreamingMovies)": int(data.no_internet_service_streaming_movies),
    "Yes (StreamingMovies)": int(data.yes_streaming_movies),
    "Month-to-month (Contract)": int(data.month_to_month_contract),
    "One year (Contract)": int(data.one_year_contract),
    "Two year (Contract)": int(data.two_year_contract),
    "No (PaperlessBilling)": int(data.no_paperless_billing),
    "Yes (PaperlessBilling)": int(data.yes_paperless_billing),
    "Bank transfer (automatic) (PaymentMethod)": int(data.bank_transfer_automatic_payment_method),
    "Credit card (automatic) (PaymentMethod)": int(data.credit_card_automatic_payment_method),
    "Electronic check (PaymentMethod)": int(data.electronic_check_payment_method),
    "Mailed check (PaymentMethod)": int(data.mailed_check_payment_method)
  }])[FEATURES]