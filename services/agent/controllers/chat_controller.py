from fastapi import HTTPException

from graph.graph import agent_graph
from utils.history_service import history_service
from utils.chat_service import chat_service


class ChatController:

    def handle(self, user_message: str, user_id: str, conversation_id: str = None, file_id: str = None) -> dict:
        
        if not conversation_id or not chat_service.conversation_exists(conversation_id):
            conversation_id = chat_service.create_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                title=user_message[:50],
            )

        history = history_service.get_history(conversation_id)

        try:
            result = agent_graph.invoke({
                "user_message": user_message,
                "conversation_id": conversation_id,
                "user_id": user_id,
                "file_id": file_id,
                "history": history,
                "intent": None,
                "response": None,
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        # save user message and assistant response
        chat_service.create_message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
            intent=result["intent"],
        )
        chat_service.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=result["response"],
            intent=result["intent"],
        )

        return {
            "conversation_id": conversation_id,
            "intent": result["intent"],
            "response": result["response"],
        }


chat_controller = ChatController()