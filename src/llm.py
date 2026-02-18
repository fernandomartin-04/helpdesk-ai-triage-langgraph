import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMError(RuntimeError):
    pass


def call_llm(prompt: str) -> dict:
    """
    Función genérica: envía un prompt al modelo y devuelve un dict (JSON).
    En Fase 5, los prompts viven en los nodos, no aquí.
    """
    token = os.getenv("HUGGINGFACE_API_KEY")
    model = os.getenv("HF_MODEL", "HuggingFaceTB/SmolLM3-3B:hf-inference")

    if not token:
        raise LLMError("Falta HUGGINGFACE_API_KEY en el .env")

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=token,
    )

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300,
            # Si el modelo no soporta response_format, quítalo.
            response_format={"type": "json_object"},
        )
    except Exception as e:
        raise LLMError(f"Error llamando al router HF: {e}") from e

    text = completion.choices[0].message.content.strip()

    json_str = _extract_json_block(text)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise LLMError(f"No pude parsear JSON. Salida fue: {text}") from e


def _extract_json_block(text: str) -> str:
    """
    1) Si el texto completo ya es JSON válido, lo devuelve tal cual.
    2) Si no, intenta extraer desde la primera { hasta la última } y valida.
    """
    text = text.strip()

    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise LLMError(f"No encontré JSON en la respuesta: {text}")

    candidate = text[start:end + 1].strip()

    try:
        json.loads(candidate)
        return candidate
    except json.JSONDecodeError as e:
        raise LLMError(f"No encontré JSON válido en la respuesta: {text}") from e



