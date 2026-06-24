from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

PROCESSED_FOLDER = Path("data/processed")
DATABASE_FILE = "bluestock_mf.db"


def main():
    engine = create_engine(f"sqlite:///{DATABASE_FILE}")

    file_to_table = {
        "01_fund_master_cleaned.csv": "dim_fund",
        "02_nav_history_cleaned.csv": "fact_nav",
        "03_aum_by_fund_house_cleaned.csv": "fact_aum",
        "04_monthly_sip_inflows_cleaned.csv": "fact_sip_inflows",
        "05_category_inflows_cleaned.csv": "fact_category_inflows",
        "06_industry_folio_count_cleaned.csv": "fact_industry_folios",
        "07_scheme_performance_cleaned.csv": "fact_performance",
        "08_investor_transactions_cleaned.csv": "fact_transactions",
        "09_portfolio_holdings_cleaned.csv": "fact_portfolio_holdings",
        "10_benchmark_indices_cleaned.csv": "fact_benchmark_indices",
    }

    for file_name, table_name in file_to_table.items():
        file_path = PROCESSED_FOLDER / file_name
        df = pd.read_csv(file_path)

        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Loaded {file_name} → {table_name}: {len(df)} rows")

    print("\nDATABASE ROW-COUNT VERIFICATION")
    with engine.connect() as connection:
        for table_name in file_to_table.values():
            row_count = connection.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar()
            print(f"{table_name}: {row_count} rows")

    print(f"\nDatabase created: {DATABASE_FILE}")


if __name__ == "__main__":
    main()