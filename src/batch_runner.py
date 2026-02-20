import os
from typing import Dict, Any, Tuple, List

from src.graph_builder import build_graph
from src.db import fetch_pending_tickets


def build_ticket_text(subject: str | None, description: str | None) -> str:
    subject = subject or ""
    description = description or ""
    return f"{subject}\n{description}".strip()


def run_batch(limit: int = 100) -> Dict[str, Any]:
    """
    Procesa tickets pendientes (tickets_raw sin salida en tickets_llm para el modelo actual).
    Devuelve un resumen de ejecución.
    """
    model = os.getenv("HF_MODEL")
    if not model:
        raise RuntimeError("Falta HF_MODEL en el entorno (.env)")

    graph = build_graph()

    pending = fetch_pending_tickets(model=model, limit=limit)

    processed = 0
    errors = 0

    for (ticket_id, subject, description) in pending:
        ticket_text = build_ticket_text(subject, description)

        try:
            graph.invoke(
                {
                    "ticket_id": str(ticket_id),
                    "ticket_text": ticket_text,
                    "model": model,
                }
            )
            processed += 1
        except Exception as e:
            # En batch, lo normal es loguear y continuar
            errors += 1
            print(f"[ERROR] ticket_id={ticket_id} -> {e}")

    return {
        "model": model,
        "requested_limit": limit,
        "found_pending": len(pending),
        "processed": processed,
        "errors": errors,
    }