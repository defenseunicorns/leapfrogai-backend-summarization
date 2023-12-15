from fastapi import FastAPI

from backends.summarize import router as summarize_router
from backends.summarize.routes import *
from backends.health import router as health_router
from backends.health.routes import *

tags_metadata = [
    {
        "name": "summarize",
        "description": "Provides a cohesive, single-paragraph summary based on the provided text.",
    },
    {
        "name": "refine",
        "description": "Refines a provided text to a particular format. Refinement can be done using the following methods: \n1. single-prompt (fastest, lower quality),\n2. multi-prompt (slowest, higher quality), and\n3. outlines (highest quality, doesn't work with all models).",
    },
    {
        "name": "summarize and refine",
        "description": "Summarizes and then refines the summary into a particular format. Refinement can be done using the following methods: \n1. single-prompt (fastest, lower quality),\n2. multi-prompt (slowest, higher quality), and\n3. outlines (highest quality, doesn't work with all models).",
    },
    {
        "name": "health",
        "description": "Provides status on this API.",
    },
    {
        "name": "upstream health",
        "description": "Provides status on the upstream API that processes the model and inferencing requests.",
        "externalDocs": {
            "description": "LeapfrogAI API",
            "url": "https://github.com/defenseunicorns/leapfrogai-api",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(summarize_router)
app.include_router(health_router)
