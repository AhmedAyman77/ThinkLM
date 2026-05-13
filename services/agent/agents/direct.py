from graph.nodes import AgentState
from utils.genai_client import genai_client

client = genai_client

def direct_agent(state: AgentState) -> AgentState:
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
    )

    return {**state, "response": response.text}