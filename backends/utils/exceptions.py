from fastapi import HTTPException
from ..utils.openai_config import LEAPFROGAI_BASE_URL

OPENAI_UNREACHABLE = HTTPException(
    status_code=502,
    detail=f"OpenAI API, or OpenAI-like API, was unreachable. Please check your connection to the provided API base URL: {LEAPFROGAI_BASE_URL}",
)

CHAIN_SUMMARIZATION_FAILED = HTTPException(
    status_code=500,
    detail=f"Chain summarization failed",
)

TEXT_CHUNKING_FAILED = HTTPException(
    status_code=500,
    detail=f"Text chunking failed",
)

TEXT_STUFFING_FAILED = HTTPException(
    status_code=500,
    detail=f"Text stuffing failed",
)

REFINE_SUMMARIZATION_FAILED = HTTPException(
    status_code=500,
    detail=f"Summarization refinement failed",
)
