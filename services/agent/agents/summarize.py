from graph.nodes import AgentState
from shared import settings, supabase_client
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

MAX_CHUNK_CHARS = 8000


def _get_user_files(user_id: str) -> list[dict]:
    response = supabase_client.table("files") \
        .select("raw_text_path, file_name") \
        .eq("user_id", user_id) \
        .eq("status", "ready") \
        .execute()
    return response.data


def _download_text(raw_text_path: str) -> str:
    content = supabase_client.storage.from_("documents").download(raw_text_path)
    return content.decode("utf-8")


def _split_into_chunks(text: str) -> list[str]:
    return [text[i:i + MAX_CHUNK_CHARS] for i in range(0, len(text), MAX_CHUNK_CHARS)]


def _map_summary(chunk: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Summarize this section concisely:\n\n{chunk}"
    )
    return response.text


def _reduce_summaries(summaries: list[str]) -> str:
    combined = "\n\n".join(summaries)
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=f"Synthesize these summaries into one cohesive summary:\n\n{combined}"
    )
    return response.text


def summarize_agent(state: AgentState) -> AgentState:
    files = _get_user_files(state["user_id"])

    if not files:
        return {**state, "response": "You have no documents uploaded yet."}

    all_summaries = []

    for file in files:
        raw_text = _download_text(file["raw_text_path"])
        chunks = _split_into_chunks(raw_text)
        file_summaries = [_map_summary(chunk) for chunk in chunks]
        all_summaries.extend(file_summaries)

    final_summary = _reduce_summaries(all_summaries)

    return {**state, "response": final_summary}