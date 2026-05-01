from graph.nodes import AgentState
from utils.qdrant_search_service import qdrant_search_service
from shared import settings
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def _embed_query(query: str) -> list[float]:
    result = client.models.embed_content(
        model=settings.EMBEDDING_MODEL_ID,
        contents=query
    )
    return result.embeddings[0].values


def rag_agent(state: AgentState) -> AgentState:
    collection_name = f"collection_{state['user_id']}"
    query_vector = _embed_query(state["user_message"])

    chunks = qdrant_search_service.search(collection_name, query_vector)

    if not chunks:
        return {**state, "response": "I don't have information about that in your documents."}

    context = "\n\n".join([chunk["text"] for chunk in chunks])

    system_prompt = f"""You are a helpful assistant. Answer the user's question using ONLY the context below.
If the answer is not in the context, say "I don't have information about that in your documents."

Context:
{context}"""

    history = state["history"]
    contents = []
    for msg in history:
        contents.append({
            "role": msg["role"],
            "parts": [{"text": msg["content"]}]
        })
    contents.append({
        "role": "user",
        "parts": [{"text": state["user_message"]}]
    })

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=contents,
        config={"system_instruction": system_prompt}
    )

    return {**state, "response": response.text}