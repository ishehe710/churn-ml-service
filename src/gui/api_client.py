import requests

PREDICT_ENDPOINT = "http://127.0.0.1:8000/predict"
TIMEOUT_SECONDS = 5


class ChurnAPIError(Exception):
    """Raised when the churn API request fails."""


def predict_churn(payload: dict) -> dict:
    try:
        response = requests.post(
            PREDICT_ENDPOINT,
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )
    except requests.exceptions.RequestException as e:
        raise ChurnAPIError(f"Failed to connect to churn API: {e}")

    if response.status_code != 200:
        raise ChurnAPIError(
            f"Churn API error {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except ValueError:
        raise ChurnAPIError("Invalid JSON response from churn API")
