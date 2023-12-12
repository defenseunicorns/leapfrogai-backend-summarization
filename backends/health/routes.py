from . import router
import httpx

from .types import Health
from ..utils.openai_client import LEAPFROGAI_HEALTH_URL
from ..utils.exceptions import OPENAI_UNREACHABLE


@router.get("/healthz")
async def healthz() -> Health:
    return Health()


@router.get("/api/healthz")
async def api_health() -> Health:
    async with httpx.AsyncClient() as client:
        response = await client.get(LEAPFROGAI_HEALTH_URL)

        if response.status_code == 200:
            return Health()
        else:
            raise OPENAI_UNREACHABLE
