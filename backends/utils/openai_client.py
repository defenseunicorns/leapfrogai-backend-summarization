from openai import OpenAI
from dotenv import load_dotenv
import os

from .base_url import get_base_url

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

LEAPFROGAI_HEALTH_URL = f"{get_base_url(LEAPFROGAI_BASE_URL)}/healthz"

openai_client_opts = {
    "base_url": LEAPFROGAI_BASE_URL,
    "api_key": LEAPFROGAI_API_KEY,
    "timeout": 1000 * 60 * 60 * 2,  # 2 hours
}

openai_prompt_opts = {
    "max_tokens": 8192,
    "temperature": 0.2,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.0,
}

openai_client = OpenAI(**openai_client_opts)
