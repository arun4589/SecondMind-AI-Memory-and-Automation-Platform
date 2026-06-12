from fastapi import APIRouter
from backend.schemas.chat import ChatRequest
from backend.services.secondmind_services import secondmind
from langchain_core.messages import HumanMessage
from config import CONFIG
from fastapi.responses import StreamingResponse
import json

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
async def chat(request: ChatRequest):
    config = {
    "configurable": {
        "thread_id": request.thread_id,
        "user_id":CONFIG['configurable']['user_id']
    }
}

    result = await secondmind.chat(
        [HumanMessage(content=request.message)],
        config=config
    )

    return {
        "response": result["messages"][-1].content
    }

@router.post("/stream")
async def stream_chat(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.thread_id,
            "user_id": "default_user"
        }
    }

    async def event_generator():

        async for msg, metadata in secondmind.stream_chat(
        [HumanMessage(content=request.message)],
        config
    ):

            if (
            metadata.get("langgraph_node") == "chat_node"
            and hasattr(msg, "content")
            and msg.content
            and str(msg.content).strip()
        ):

                yield (
                f"data: {json.dumps({'token': msg.content})}\n\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )