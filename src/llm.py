import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMError(RuntimeError):
    pass


def call_llm(ticket_text: str) -> dict:
    token = os.getenv("HUGGINGFACE_API_KEY")
    model = os.getenv("HF_MODEL", "HuggingFaceTB/SmolLM3-3B:hf-inference")

    if not token:
        raise LLMError("Falta HUGGINGFACE_API_KEY en el .env")

    # 👉 Cliente apuntando al router de Hugging Face
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=token,
    )

    instruction = """
    Eres un sistema de clasificación automática.

    IMPORTANTE:
    - No expliques tu razonamiento.
    - No uses etiquetas como <think>.
    - No escribas texto adicional.
    - No escribas comentarios.
    - Devuelve únicamente un objeto JSON válido.
    - No incluyas nada antes ni después del JSON.

    El JSON debe tener exactamente esta estructura:

    {
      "ticket_type": "...",
      "ticket_priority": "...",
      "rationale": "..."
    }

    Ticket Type debe ser uno de:
    - Technical issue
    - Billing inquiry
    - Cancellation request
    - Product inquiry
    - Refund request

    Ticket Priority debe ser uno de:
    - Critical
    - High
    - Medium
    - Low
    """

    prompt = f"{instruction}\n\nTICKET:\n{ticket_text}\n\nJSON:"

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200,
            response_format={"type": "json_object"},
        )

    except Exception as e:
        raise LLMError(f"Error llamando al router HF: {e}") from e

    text = completion.choices[0].message.content.strip()

    json_str = _extract_json_block(text)

    try:
        result = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise LLMError(f"No pude parsear JSON. Salida fue: {text}") from e

    return result


def _extract_json_block(text: str) -> str:
    """
    Extrae el primer bloque JSON válido de un texto.
    """
    import re

    matches = re.findall(r'\{.*?\}', text, re.DOTALL)
    for match in matches:
        try:
            json.loads(match)
            return match
        except json.JSONDecodeError:
            continue

    raise LLMError(f"No encontré JSON válido en la respuesta: {text}")

