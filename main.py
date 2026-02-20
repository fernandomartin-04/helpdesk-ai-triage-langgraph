from pathlib import Path
import os

from src.inspection import load_data
from src.preprocessing import preprocess
from src.graph_builder import build_graph
from src.db import init_db, upsert_raw_tickets

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data' / 'customer_support_tickets.csv'

def build_ticket_text(row):
    return f"{row['Ticket Subject']}\n{row['Ticket Description']}"

def main():
    init_db()

    raw_df = load_data(DATA_PATH)
    processed_df = preprocess(raw_df)

    # guarda CSV (una vez; INSERT OR IGNORE evita duplicados)
    upsert_raw_tickets(processed_df.to_dict(orient = 'records'))

    # construct a single ticket text, ticket ID, and model
    row = processed_df.iloc[11]
    ticket_text = build_ticket_text(row)

    # call LLM
    graph = build_graph()
    out = graph.invoke({"ticket_id": str(row['Ticket ID']), "ticket_text": ticket_text, "model": os.getenv('HF_MODEL')})
    print(out)




if __name__ == '__main__':
    main()


