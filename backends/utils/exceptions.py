from fastapi import HTTPException
from ..utils.openai_client import LEAPFROGAI_BASE_URL

OPENAI_UNREACHABLE = HTTPException(
    status_code=500,
    detail=f"OpenAI API, or OpenAI-like API, was unreachable. Please check your connection to the provided API base URL: {LEAPFROGAI_BASE_URL}",
)
