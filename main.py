from pathlib import Path

from src.inspection import load_data
from src.preprocessing import preprocess
from src.llm import call_llm
from src.graph_builder import build_graph
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data' / 'customer_support_tickets.csv'

def build_ticket_text(row):
    return f"{row['Ticket Subject']}\n{row['Ticket Description']}"


def main():
    raw_df = load_data(DATA_PATH)

    # preprocess data
    processed_df = preprocess(raw_df)

    # construct a single ticket text
    row = processed_df.iloc[10]
    ticket_text = build_ticket_text(row)

    # call LLM
    graph = build_graph()
    out = graph.invoke({"ticket_text": ticket_text})
    print(out)




if __name__ == '__main__':
    main()


