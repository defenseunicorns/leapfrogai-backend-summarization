from . import router
from .types import (
    SummarizationRequest,
    RefinementRequest,
    SummarizationResponse,
    RefinementResponse,
    SummarizeAndRefineResponse,
)
from .langchain import summarize, unguided_refine
from .guidance import guided_refine


@router.post("/summarize", tags=["summarize"])
def summarization(req: SummarizationRequest) -> SummarizationResponse:
    summary = summarize(model=req.model, text=req.text.strip())
    return {"summary": summary}


@router.post("/refine", tags=["refine"])
def refinement(req: RefinementRequest) -> RefinementResponse:
    refined_summary = ""
    if req.refine_method == "unguided":
        refined_summary = unguided_refine(text=req.text.strip(), model=req.model)
    else:
        refined_summary = guided_refine(text=req.text.strip())

    return {"refined_summary": refined_summary}


@router.post("/summarize-and-refine", tags=["summarize and refine"])
def summarize_and_refine(
    req: RefinementRequest,
) -> SummarizeAndRefineResponse:
    summary = summarize(text=req.text.strip(), model=req.model)

    refined_summary = ""
    if req.refine_method == "unguided":
        refined_summary = unguided_refine(text=summary, model=req.model)
    else:
        refined_summary = guided_refine(text=summary)

    return {"summary": summary, "refined_summary": refined_summary}
