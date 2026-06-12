from fastapi import APIRouter
from backend.services.secondmind_services import secondmind

router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


@router.get("/{user_id}")
async def get_memory(user_id: str):

    ns = ("user", user_id, "details")

    items = await secondmind.store.asearch(ns)

    memories = []

    for item in items:
        memories.append(
            item.value.get("data", "")
        )

    return {
        "memories": memories
    }