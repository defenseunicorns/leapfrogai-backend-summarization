from fastapi import HTTPException
from . import router
from .types import (
    CompletionRequest,
    ModelResponse,
)
from .langchain_summarize import summarize
from ..utils.openai_client import openai_client
from ..utils.exceptions import OPENAI_UNREACHABLE


@router.post("/summarize")
async def complete(req: CompletionRequest):
    await summarize(req)
    return req


@router.get("/models")
async def models() -> ModelResponse:
    try:
        res = openai_client.models.list()
    except:
        raise OPENAI_UNREACHABLE
    return res
