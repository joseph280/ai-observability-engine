from typing import Dict

from app.schemas.conversation import Conversation


class ConversationStore:
    def __init__(self):
        self._store: Dict[str, Conversation] = {}

    def get(self, conversation_id: str) -> Conversation | None:
        return self._store.get(conversation_id)
    
    def save(self, conversation: Conversation):
        self._store[conversation.id] = conversation