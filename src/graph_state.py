from typing import TypedDict

class TicketState(TypedDict, total = False):
    # Input (siempre está)
    ticket_id: str
    ticket_text: str
    model: str

    # Outputs (se van llenando por nodos)
    ticket_type: str
    ticket_priority: str
    summary: str
    suggested_response: str