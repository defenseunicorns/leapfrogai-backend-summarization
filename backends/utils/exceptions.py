from fastapi import HTTPException
from ._openai import LEAPFROGAI_BASE_URL

NOT_A_URL = HTTPException(
    status_code=422,
    detail=f"{LEAPFROGAI_BASE_URL} is not a proper URL",
)

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

SINGLE_PROMPT_REFINE_SUMMARIZATION_FAILED = HTTPException(
    status_code=500,
    detail=f"Single prompt summarization refinement failed",
)

MULTI_PROMPT_REFINE_SUMMARIZATION_FAILED = HTTPException(
    status_code=500,
    detail=f"Multi prompt summarization refinement failed",
)

REFINE_SUMMARIZATION_METHOD_DOES_NOT_EXIST = HTTPException(
    status_code=500,
    detail=f"Request summarization refinement method is not s supported method",
)
