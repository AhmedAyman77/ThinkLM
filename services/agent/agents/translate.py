from graph.nodes import AgentState
from shared import settings
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def translate_agent(state: AgentState) -> AgentState:
    system_prompt = """You are a translator. The user will ask you to translate content.
Detect the target language from their request and translate accurately.
Return only the translated content, nothing else."""

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=state["user_message"],
        config={"system_instruction": system_prompt}
    )

    return {**state, "response": response.text}