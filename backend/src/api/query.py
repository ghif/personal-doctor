from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.models.models import UserQuery
from src.services import query_service

router = APIRouter()

@router.post("/query")
async def query(user_query: UserQuery):
    return StreamingResponse(query_service.process_query(user_query), media_type="text/event-stream")
