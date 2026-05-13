from transformers import AutoTokenizer, AutoModelForCausalLM
from shared import settings

print("loading translation model...")

finetuned_tokenizer = AutoTokenizer.from_pretrained(settings.FINETUNED_TRANSLATE_MODEL_ID)
finetuned_model = AutoModelForCausalLM.from_pretrained(
    settings.FINETUNED_TRANSLATE_MODEL_ID,
    torch_dtype="auto",
    device_map="auto"
)

print(f"Translation model loaded from {settings.FINETUNED_TRANSLATE_MODEL_ID}")


def translate(message: str) -> str:
    inputs = finetuned_tokenizer.apply_chat_template(
        message,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )

    outputs = finetuned_model.generate(**inputs, max_new_tokens=1024)
    response = finetuned_tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])

    return response