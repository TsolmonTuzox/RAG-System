from datetime import datetime
from ..models.chat import ChatMessage

class ChatService:
    async def process_message(self, message: ChatMessage):
        return {
            "content": f"You said: {message.content}",
            "role": "assistant",
            "timestamp": datetime.now()
        }