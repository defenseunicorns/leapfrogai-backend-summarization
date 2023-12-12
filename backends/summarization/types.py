from __future__ import annotations

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


class SummarizationResponse(BaseModel):
    summary: str


##########
# MODELS
##########


class ModelResponseModel(BaseModel):
    id: str
    object: str = "model"
    created: int = 0
    owned_by: str = "leapfrogai"


class ModelResponse(BaseModel):
    object: str = "list"
    data: list[ModelResponseModel] = []
