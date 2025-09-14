from pydantic import BaseModel
from datetime import datetime


class ChatMessage(BaseModel):
    content: str
    role: str = "user"
    timestamp: datetime = datetime.now()
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "content": "How can I validate my EIN?",
                "role": "user",
                "user_id": 1,
            }
        }
