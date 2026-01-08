"""
validators.py

Owns:
- Valdiation of customer churn input for model

Does NOT:
- Load or train models
- Perform predictions
- Know about FastAPI
- Peprocessing 
- Implements feature contract/schema
- Logging configuration
"""

from src.api.schema import ChurnInput

class ValidationError(ValueError):
    pass

def validate_mutual_exclusivity(data: ChurnInput) -> None:
    
    # flags
    gender_flags = [
        data.male,
        data.female
    ]
    
    partner_flags = [
        data.no_partner,
        data.yes_partner
    ]
    
    dependents_flags = [
        data.yes_dependents,
        data.no_dependents
    ]
    
    phone_service_flags = [
        data.yes_phone_service,
        data.no_phone_service
    ]
    
    multiple_lines_flags = [
        data.yes_multiple_lines,
        data.no_phone_service_multiple_lines,
        data.no_multiple_lines
    ]
    
    internet_service_flags = [
        data.dsl_internet_service,
        data.fiber_optic_internet_service,
        data.no_internet_service
    ]
    
    online_security_flags = [
        data.no_online_security,
        data.no_internet_service_online_security,
        data.yes_online_security
    ]
    
    online_backup_flags = [
        data.no_online_backup,
        data.no_internet_service_online_backup,
        data.yes_online_backup
    ]
    
    device_protection_flags = [
        data.no_device_protection,
        data.no_internet_service_device_protection,
        data.yes_device_protection
    ]
    
    tech_support_flags = [
        data.no_tech_support,
        data.no_internet_service_tech_support,
        data.yes_tech_support
    ]
    
    streaming_movies_flags = [
        data.no_streaming_movies,
        data.no_internet_service_streaming_movies,
        data.yes_streaming_movies
    ]
    
    streaming_tv_flags = [
        data.no_streaming_tv,
        data.no_internet_service_streaming_tv,
        data.yes_streaming_tv
    ]
    
    contract_flags = [
        data.month_to_month_contract,
        data.one_year_contract,
        data.two_year_contract,
    ]
    
    paperless_billing_flags = [
        data.yes_paperless_billing,
        data.no_paperless_billing
    ]
    
    payment_method_flags = [
        data.bank_transfer_automatic_payment_method,
        data.credit_card_automatic_payment_method,
        data.mailed_check_payment_method,
        data.electronic_check_payment_method
    ]
    
    flag_groups = {
        "gender": gender_flags,
        "partner": partner_flags,
        "dependents": dependents_flags,
        "phone_service": phone_service_flags,
        "multiple_lines": multiple_lines_flags,
        "internet_service": internet_service_flags,
        "online_security": online_security_flags,
        "online_backup": online_backup_flags,
        "device_protection": device_protection_flags,
        "tech_support": tech_support_flags,
        "streaming_tv": streaming_tv_flags,
        "streaming_movies": streaming_movies_flags,
        "contract": contract_flags,
        "paperless_billing": paperless_billing_flags,
        "payment_method": payment_method_flags,
    }

    # ensures exclusivity of features
    for group_name, group_flags in flag_groups.items():
        if sum(group_flags) != 1:
            raise ValidationError(
                f"Exactly one option must be selected for '{group_name}'"
            )

