from __future__ import annotations
from typing import Literal

from pydantic import BaseModel, validator


##########
# GENERIC
##########


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int | None = None
    total_tokens: int


##########
# SUMMARIZATION
##########


class SummarizationRequest(BaseModel):
    model: str
    text: str | list[int]

    @validator("text")
    def text_must_exist(cls, v: str):
        if len(v.strip()) <= 0:
            raise ValueError("Text to be summarized must not be empty.")
        return v


class RefinementRequest(SummarizationRequest):
    refine_method: Literal["unguided", "guided"] = "unguided"


class SummarizationResponse(BaseModel):
    summary: str


class RefinementResponse(BaseModel):
    refined_summary: str


class SummarizeAndRefineResponse(BaseModel):
    summary: str
    refined_summary: str
