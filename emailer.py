# emailer.py
import httpx
from config import settings

def send_email(to: str, subject: str, body: str):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "from": "onboarding@resend.dev",
        "to": [to],
        "subject": subject,
        "html": body
    }

    # Production environment → send real email
    if settings.PRODUCTION:
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=data)
            response.raise_for_status()
    else:
        # Development mode → no API call
        print("DEV MODE: Email send simulated →")
        print(data)
