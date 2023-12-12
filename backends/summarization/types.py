from __future__ import annotations

from pydantic import BaseModel


##########
# GENERIC
##########
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int | None = None
    total_tokens: int


##########
# COMPLETION
##########
class CompletionRequest(BaseModel):
    model: str
    prompt: str | list[int]
    stream: bool | None = False
    max_tokens: int | None = 16
    temperature: float | None = 1.0


class CompletionChoice(BaseModel):
    index: int
    text: str
    logprobs: object = None
    finish_reason: str = ""


class CompletionResponse(BaseModel):
    id: str = ""
    object: str = "completion"
    created: int = 0
    model: str = ""
    choices: list[CompletionChoice]
    usage: Usage | None = None

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