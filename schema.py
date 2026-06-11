from typing import TypedDict, Annotated,List
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ChatbotState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
    summary: str

class MemoryItem(BaseModel):
    text: str = Field(description="Atomic user memory")
    is_new: bool = Field(description="True if new, false if duplicate")


class MemoryDecision(BaseModel):
    should_write: bool
    memories: List[MemoryItem] = Field(default_factory=list)        