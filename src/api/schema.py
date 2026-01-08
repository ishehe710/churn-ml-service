"""
schema.py

Owns:
- Contract customer input for the model

Does NOT:
- Load models
- Perform predictions
- Know about FastAPI
"""

from pydantic import BaseModel

"""
    Input schema for churn prediction.
    Must exactly match the 46-feature training schema.
    All features are model-ready (post-encoding).
"""
class ChurnInput(BaseModel):
    senior_citizen: int
    tenure: int
    monthly_charges: float
    total_charges: float
    
    # one-hot encoding (they are boolean values really)
    female: int
    male: int
    no_partner: int
    yes_partner: int
    no_dependents: int
    yes_dependents: int
    no_phone_service: int
    yes_phone_service: int
    no_multiple_lines: int
    no_phone_service_multiple_lines: int
    yes_multiple_lines: int
    dsl_internet_service: int
    fiber_optic_internet_service: int
    no_internet_service: int
    no_online_security: int
    no_internet_service_online_security: int
    yes_online_security: int
    no_online_backup: int
    no_internet_service_online_backup: int
    yes_online_backup: int
    no_device_protection: int
    no_internet_service_device_protection: int
    yes_device_protection: int
    no_tech_support: int
    no_internet_service_tech_support: int
    yes_tech_support: int
    no_streaming_tv: int
    no_internet_service_streaming_tv: int
    yes_streaming_tv: int
    no_streaming_movies: int
    no_internet_service_streaming_movies: int
    yes_streaming_movies: int
    month_to_month_contract: int
    one_year_contract: int
    two_year_contract: int
    no_paperless_billing: int
    yes_paperless_billing: int
    bank_transfer_automatic_payment_method: int
    credit_card_automatic_payment_method: int
    electronic_check_payment_method: int
    mailed_check_payment_method: int