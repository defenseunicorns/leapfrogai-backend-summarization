from . import router
from .types import (
    SummarizationRequest,
    SummarizationResponse,
    RefinementResponse,
    SummarizeAndRefineResponse,
)
from .summarize import summarize, refine


@router.post("/summarize", tags=["summarize"])
def summarization(req: SummarizationRequest) -> SummarizationResponse:
    summary = summarize(model=req.model, text=req.text.strip())
    return {"summary": summary}


@router.post("/refine", tags=["refine"])
def refinement(req: SummarizationRequest) -> RefinementResponse:
    refined_summary = refine(model=req.model, text=req.text.strip())
    return {"refine": refined_summary}


@router.post("/summarize-and-refine", tags=["summarize and refine"])
def summarization_and_refinement(
    req: SummarizationRequest,
) -> SummarizeAndRefineResponse:
    summary = summarize(model=req.model, text=req.text.strip())
    refined_summary = refine(model=req.model, text=summary)
    return {"summary": summary, "refined_summary": refined_summary}
