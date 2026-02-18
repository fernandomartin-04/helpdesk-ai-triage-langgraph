from src.llm import call_llm

TICKET_TYPES = [
    "Technical issue",
    "Billing inquiry",
    "Cancellation request",
    "Product inquiry",
    "Refund request",
]

TICKET_PRIORITIES = ["Critical", "High", "Medium", "Low"]


def classify_node(state: dict) -> dict:
    """
    Input:  state["ticket_text"]
    Output: {"ticket_type": ..., "ticket_priority": ...}
    """
    prompt = f"""
Eres un sistema de clasificación de tickets.

Devuelve SOLO JSON válido con esta estructura:
{{
  "ticket_type": "...",
  "ticket_priority": "..."
}}

Ticket Type debe ser uno de:
{TICKET_TYPES}

Ticket Priority debe ser uno de:
{TICKET_PRIORITIES}

No incluyas texto fuera del JSON.

TICKET:
{state["ticket_text"]}

JSON:
""".strip()

    result = call_llm(prompt)

    return {
        "ticket_type": result["ticket_type"],
        "ticket_priority": result["ticket_priority"],
    }


def summarize_node(state: dict) -> dict:
    """
    Input:  state["ticket_text"]
    Output: {"summary": ...}
    """
    prompt = f"""
Resume el ticket en UNA frase corta (máx 20 palabras).
Devuelve SOLO JSON válido con esta estructura:
{{
  "summary": "..."
}}

No incluyas texto fuera del JSON.

TICKET:
{state["ticket_text"]}

JSON:
""".strip()

    result = call_llm(prompt)

    return {"summary": result["summary"]}


def generate_reply_node(state: dict) -> dict:
    """
    Input:  state["ticket_text"], state["ticket_type"], state["ticket_priority"], state["summary"]
    Output: {"suggested_response": ...}
    """
    prompt = f"""
Eres un agente de soporte.

Contexto:
- Ticket Type: {state["ticket_type"]}
- Ticket Priority: {state["ticket_priority"]}
- Summary: {state["summary"]}

Escribe una respuesta sugerida educada y útil (2 a 5 frases).
Devuelve SOLO JSON válido con esta estructura:
{{
  "suggested_response": "..."
}}

No incluyas texto fuera del JSON.

TICKET:
{state["ticket_text"]}

JSON:
""".strip()

    result = call_llm(prompt)

    return {"suggested_response": result["suggested_response"]}
