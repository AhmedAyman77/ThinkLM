from typing import TypedDict, Optional
from google import genai
from shared import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class AgentState(TypedDict):
    user_message: str
    conversation_id: str
    user_id: str
    history: list[dict]
    intent: Optional[str]
    response: Optional[str]


def classify_intent(state: AgentState) -> AgentState:
    system_prompt = """You are an intent classifier. Classify the user message into exactly one of these intents:

RAG_QUERY — user is asking a question about their uploaded documents.
Examples:
- "What does the contract say about termination?"
- "What are the key findings in the report?"
- "Does the document mention payment terms?"

SUMMARIZE — user wants a summary of their uploaded documents.
Examples:
- "Summarize my documents"
- "Give me an overview of what I uploaded"
- "What is this document about?"

TRANSLATE — user wants content translated to another language.
Examples:
- "Translate this to Arabic"
- "Can you translate the document to French?"
- "What does this say in Spanish?"

DIRECT_LLM — general conversation, greetings, or anything unrelated to documents.
Examples:
- "Hello"
- "What is the capital of France?"
- "Tell me a joke"
- "How are you?"

Respond with ONLY the intent name. Nothing else. No explanation. No punctuation.
Correct: RAG_QUERY
Wrong: "RAG_QUERY" or "The intent is RAG_QUERY" """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=state["user_message"],
        config={"system_instruction": system_prompt}
    )

    intent = response.text.strip()

    valid_intents = ["RAG_QUERY", "SUMMARIZE", "TRANSLATE", "DIRECT_LLM"]
    if intent not in valid_intents:
        intent = "DIRECT_LLM"

    return {**state, "intent": intent}


def route_intent(state: AgentState) -> str:
    return state["intent"]