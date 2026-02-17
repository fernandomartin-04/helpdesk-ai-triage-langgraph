from pathlib import Path

from src.inspection import load_data
from src.preprocessing import preprocess
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data' / 'customer_support_tickets.csv'


def main():
    raw_df = load_data(DATA_PATH)

    # preprocess data
    processed_df = preprocess(raw_df)


if __name__ == '__main__':
    main()

