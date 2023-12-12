from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

LEAPFROGAI_BASE_URL = os.getenv("LEAPFROGAI_BASE_URL")
LEAPFROGAI_API_KEY = os.getenv("LEAPFROGAI_API_KEY")

if LEAPFROGAI_API_KEY is None:
    raise EnvironmentError(
        f"Required environment variable LEAPFROGAI_API_KEY not found"
    )

if LEAPFROGAI_BASE_URL is None:
    raise EnvironmentError(
        f"Required environment variable LEAPFROGAI_BASE_URL not found"
    )

openai_client = OpenAI(
    base_url=LEAPFROGAI_BASE_URL,
    api_key=LEAPFROGAI_API_KEY,
    timeout=1000 * 60 * 60 * 2,  # 2 hours
)
