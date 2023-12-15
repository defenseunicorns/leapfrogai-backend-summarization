from __future__ import annotations

from pydantic import BaseModel

##########
# Health
##########
class Health(BaseModel):
    status: str = "ok"