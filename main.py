from pathlib import Path

from src.inspection import load_data
from src.preprocessing import preprocess
from src.llm import call_llm
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data' / 'customer_support_tickets.csv'


def main():
    raw_df = load_data(DATA_PATH)

    # preprocess data
    processed_df = preprocess(raw_df)

    # construct a single ticket text
    row = processed_df.iloc[2]
    ticket_text = f"{row['Ticket Subject']}\n{row['Ticket Description']}"

    # call LLM
    prediction = call_llm(ticket_text)

    print("=== TICKET ===")
    print(ticket_text)
    print("\n=== PREDICCIÓN ===")
    print(prediction)

    print("\n=== VALORES REALES ===")
    print("Tipo real:", row["Ticket Type"])
    print("Prioridad real:", row["Ticket Priority"])



if __name__ == '__main__':
    main()


