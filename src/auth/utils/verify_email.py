import requests

from src.config import settings


EMAILHUNTER_BASE_URL = "https://api.emailhunter.co/v2"


def verify_email(email: str):
    url = f"{EMAILHUNTER_BASE_URL}/email-verifier?email={email}&api_key={settings.EMAIL_VERIFIER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        if data["data"]["result"] == "deliverable":
            return True
        else:
            return False
    return False
