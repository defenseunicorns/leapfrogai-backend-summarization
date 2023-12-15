from typing import Dict, Literal
from enum import Enum


from pydantic import BaseModel, validator


#######
# USAGE
#######


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int | None = None
    total_tokens: int


###############
# SUMMARIZATION
###############


class SummarizationRequest(BaseModel):
    model: str
    text: str | list[int]

    @validator("text")
    def text_must_exist(cls, v: str):
        if len(v.strip()) <= 0:
            raise ValueError("Text to be summarized must not be empty.")
        return v


class SummarizationResponse(BaseModel):
    summary: str


############
# REFINEMENT
############

AVAILABLE_REFINEMENT_OPTIONS = Literal["single-prompt", "multi-prompt", "outlines"]

DEFAULT_REFINEMENT_OPTION = "single-prompt"

DEFAULT_SECTIONS = {
    "BLUF": "this section will be a concise, one paragraph executive summary of the text.",
    "NOTES": "this section will be a bullet points highlighting and summarizing key points, risks, issues, and opportunities from the text.",
    "ACTIONS": "this section will be a bulleted list of open action items or unanswered questions that exist from the text.",
}

SECTIONS = Dict[str, str] 

class RefinementRequest(SummarizationRequest):
    refine_method: AVAILABLE_REFINEMENT_OPTIONS = DEFAULT_REFINEMENT_OPTION
    sections: SECTIONS = DEFAULT_SECTIONS


class RefinementResponse(BaseModel):
    refined_summary: str
    refine_method: AVAILABLE_REFINEMENT_OPTIONS = DEFAULT_REFINEMENT_OPTION


##############################
# SUMMARIZATION AND REFINEMENT
##############################


class SummarizeAndRefineResponse(RefinementResponse):
    summary: str
