from shared import supabase_client

class HistoryService:

    def get_history(self, conversation_id: str) -> list[dict]:
        response = supabase_client.table("messages") \
            .select("role, content") \
            .eq("conversation_id", conversation_id) \
            .order("created_at", desc=True) \
            .limit(7) \
            .execute()

        messages = response.data[::-1]
        return messages

history_service = HistoryService()