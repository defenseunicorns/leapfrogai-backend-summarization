from . import router
from .lib.types import (
    SummarizationRequest,
    RefinementRequest,
    SummarizationResponse,
    RefinementResponse,
    SummarizeAndRefineResponse,
)
from .lib.summarization.summarize import summarize
from .lib.refinement.refine import refine


@router.post("/summarize", tags=["summarize"])
def summarization(req: SummarizationRequest) -> SummarizationResponse:
    summary = summarize(model=req.model, text=req.text.strip())
    return {"summary": summary}


@router.post("/refine", tags=["refine"])
def refinement(req: RefinementRequest) -> RefinementResponse:
    refined_summary = refine(
        text=req.text.strip(),
        model=req.model,
        sections=req.sections,
        refine_method=req.refine_method,
    )

    return {"refined_summary": refined_summary, "refine_method": req.refine_method}


@router.post("/summarize-and-refine", tags=["summarize and refine"])
def summarize_and_refine(
    req: RefinementRequest,
) -> SummarizeAndRefineResponse:
    summary = summarize(text=req.text.strip(), model=req.model)
    refined_summary = refine(
        text=summary,
        model=req.model,
        sections=req.sections,
        refine_method=req.refine_method,
    )

    return {"summary": summary, "refined_summary": refined_summary, "refine_method": req.refine_method}
