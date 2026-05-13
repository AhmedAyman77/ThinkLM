from graph.nodes import AgentState
from shared import supabase_client, SupabaseEnum
from utils.summarize_model import summarize
from utils.genai_client import genai_client

client = genai_client

def download_text(raw_text_path: str) -> str:
    content = supabase_client.storage.from_(SupabaseEnum.STORAGE_BUCKET.value).download(raw_text_path)
    return content.decode("utf-8")

def get_file(file_id: str, user_id: str) -> str:
    response = supabase_client.table("files") \
        .select("content_path") \
        .eq("user_id", user_id) \
        .eq("id", file_id) \
        .eq("status", "ready") \
        .single() \
        .execute()

    return response.data["content_path"] if response.data else None

def get_random_file(user_id: str) -> str:
    response = supabase_client.table("files") \
        .select("content_path") \
        .eq("user_id", user_id) \
        .eq("status", "ready") \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()

    return response.data["content_path"] if response.data else None

def summarize_agent(state: AgentState) -> AgentState:
    file_id = state["file_id"]
    user_id = state["user_id"]

    # get file

    if file_id:
        content_path = get_file(file_id, user_id)
    else:
        content_path = get_random_file(user_id)
    
    # get content
    raw_text = download_text(content_path)

    # generate summary
    system_message = "\n".join([
        "You are a concise text summarizer.",
        "You will be provided with a text to summarize.",
        "Generate the summary in the same language as the input text.",
        "Capture the key points and main ideas accurately.",
        "Return only the summary with no introduction or conclusion."
    ])

    message = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": "\n".join([
                    "Original Text:",
                    raw_text,
                ])
        },
    ]

    final_summary = summarize(message)

    return {**state, "response": final_summary}