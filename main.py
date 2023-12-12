from fastapi import FastAPI

from backends.summarization import router as summarization_router
from backends.summarization.routes import *
from backends.health import router as health_router
from backends.health.routes import *

app = FastAPI()

app.include_router(summarization_router)
app.include_router(health_router)

