from pathlib import Path

from src.inspection import load_data
from src.preprocessing import preprocess
from src.db import init_db, upsert_raw_tickets
from src.batch_runner import run_batch

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "customer_support_tickets.csv"


def main():
    # 1️⃣ Inicializar base
    init_db()

    # 2️⃣ Cargar datos y guardarlos en tickets_raw
    raw_df = load_data(DATA_PATH)
    processed_df = preprocess(raw_df)
    upsert_raw_tickets(processed_df.to_dict(orient="records"))

    # 3️⃣ Procesamiento en lote
    result = run_batch(limit=100)
    print("Batch result:", result)


if __name__ == "__main__":
    main()

