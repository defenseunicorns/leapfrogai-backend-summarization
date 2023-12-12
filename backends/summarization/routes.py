from . import router
from .types import (
    SummarizationRequest,
    SummarizationResponse,
)
from .summarize import summarize


@router.post("/summarize")
def complete(req: SummarizationRequest) -> SummarizationResponse:
    summary = summarize(model=req.model, text=req.text.strip())
    return {"summary": summary}
