from graph.nodes import AgentState
from utils.genai_client import genai_client
from utils.translation_model import translate
from langdetect import detect

client = genai_client

def language_detect(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"

def system_message(language: str) -> str:
    arabic_system_message = "\n".join([
        "أنت مترجم محترف.",
        "ترجم النص المقدم بدقة الى اللغه العربيه.",
        "حافظ على المعنى الأصلي والأسلوب والسياق.",
        "اكتب الترجمة فقط — بدون شرح أو مقدمة أو أي نص إضافي."
    ])
    english_system_message = "\n".join([
        "You are a professional translator.",
        "Translate the provided text accurately in english.",
        "Preserve the original meaning, tone, and style.",
        "Output only the translation — no explanations, no introductions, no extra text."
    ])

    if language == "ar":
        return arabic_system_message

    return english_system_message


def translate_agent(state: AgentState) -> AgentState:
    system_prompt = system_message(language_detect(state["user_message"]))
    user_message = state["user_message"]

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "\n".join([
                        "Original Text:",
                        user_message,
                    ])
        },
    ]
    
    response = translate(messages)

    return {**state, "response": response}