import uuid
from graph.graph import agent_graph
from utils.history_service import history_service
from utils.message_service import message_service


class ChatController:

    def handle(self, user_message: str, user_id: str, conversation_id: str = None) -> dict:

        # create conversation if it does not exist
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        if not message_service.conversation_exists(conversation_id):
            message_service.create_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                title=user_message[:50],
            )

        # get last 7 messages
        history = history_service.get_history(conversation_id)

        # run the graph
        result = agent_graph.invoke({
            "user_message": user_message,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "history": history,
            "intent": None,
            "response": None,
        })

        # save user message and assistant response
        message_service.create_message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
            intent=result["intent"],
        )
        message_service.create_message(
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