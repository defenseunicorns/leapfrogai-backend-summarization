from . import router
from .types import (
    SummarizationRequest,
    SummarizationResponse,
    ModelResponse,
)
from .summarize import summarize
from ..utils.openai_client import openai_client
from ..utils.exceptions import OPENAI_UNREACHABLE


@router.post("/summarize")
def complete(req: SummarizationRequest) -> SummarizationResponse:
    summary = summarize(model=req.model, text=req.text)
    return {"summary": summary}


@router.get("/models")
async def models() -> ModelResponse:
    try:
        res: ModelResponse = openai_client.models.list()
    except:
        raise OPENAI_UNREACHABLE
    return res
