from fastapi import APIRouter
from backend.schemas.chat import ChatRequest
from backend.services.secondmind_services import secondmind
from langchain_core.messages import HumanMessage
from config import CONFIG

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
async def chat(request: ChatRequest):

    result = await secondmind.chat(
        [HumanMessage(content=request.message)],
        CONFIG
    )

    return {
        "response": result["messages"][-1].content
    }