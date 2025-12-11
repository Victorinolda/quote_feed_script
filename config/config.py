import os
from dotenv import load_dotenv

load_dotenv()


TOKEN_PISTIS = os.getenv("TOKEN_PISTIS", None)
TOKEN_BLUEPILL = os.getenv("TOKEN_BLUEPILL", None)
QUOTE_ID = os.getenv("QUOTE_ID", "")

if not TOKEN_PISTIS:
    raise ValueError("TOKEN_PISTIS environment variable is not set.")
if not TOKEN_BLUEPILL:
    raise ValueError("TOKEN_BLUEPILL environment variable is not set.")
if not QUOTE_ID or QUOTE_ID == "":
    raise ValueError("QUOTE_ID environment variable is not set.")

TOKEN_PLUTUS = f"Bearer {TOKEN_PISTIS}"

PLUTUS_HOST = os.getenv("PLUTUS_HOST", "http://localhost:3002")

TIMESTAMP = os.getenv("TIMESTAMP", "2025-06-02T13:59:56.903Z")
BLUEPILL_HOST = os.getenv("BLUEPILL_HOST", "http://localhost:8004")
SECUTIRY_URL = f"{BLUEPILL_HOST}/api/v0/security-extended/?page_size=100"

URL_PLUTUS = f"{PLUTUS_HOST}/v1/feed/quote"


HEADERS = {
    "Authorization": TOKEN_PLUTUS,
    "content-type": "application/json",
}

SLEEP_TIME_POST_QUOTE_FEED = float(os.getenv("SLEEP_TIME_POST_QUOTE_FEED", 1))
ISIN = os.getenv("ISIN", "MX0MGO0001E4")  # Default ISIN
NUMBER_OF_QUOTES = int(os.getenv("NUMBER_OF_QUOTES", 10))  # Default number of quotes
ENV = os.getenv("ENV", "local")
