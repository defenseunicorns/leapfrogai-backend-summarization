from . import router
from .types import Health

from ..utils.openai_client import openai_client
from ..utils.exceptions import OPENAI_UNREACHABLE


@router.get("/healthz")
async def healthz() -> Health:
    return Health()


@router.get("/api-health")
async def api_health() -> Health:
    try:
        openai_client.models.list()
        return Health()
    except:
        raise OPENAI_UNREACHABLE
