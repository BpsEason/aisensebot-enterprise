from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    user_id: str
    text: str

@router.post("/message")
async def process_message(message: ChatMessage) -> Dict[str, Any]:
    """
    Processes a user message via REST API.
    """
    mock_response = {
        "intent": "greet",
        "slots": {
            "name": "User"
        }
    }
    return mock_response
