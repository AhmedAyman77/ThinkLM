import uuid
from shared import supabase_client

class MessageService:

    def create_message(self, conversation_id: str, role: str, content: str, intent: str = None, modality: str = "text"):
        message_id = str(uuid.uuid4())
        supabase_client.table("messages").insert({
            "id": message_id,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "intent": intent,
            "modality": modality
        }).execute()
    
        return message_id
    
    def create_conversation(self, conversation_id: str, user_id: str, title: str = "New Conversation") -> str:
        supabase_client.table("conversations").insert({
            "id": conversation_id,
            "user_id": user_id,
            "title": title
        }).execute()
    
    def conversation_exists(self, conversation_id: str) -> bool:
        response = supabase_client.table("conversations").select("id").eq("id", conversation_id).execute()
        return len(response.data) > 0

message_service = MessageService()