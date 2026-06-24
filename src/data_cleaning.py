from pathlib import Path
import pandas as pd

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")


def clean_nav_history(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    df = df.drop_duplicates()
    df = df.sort_values(["amfi_code", "date"])

    # Fill missing NAV values within each fund, if any exist
    df["nav"] = df.groupby("amfi_code")["nav"].ffill()

    # Keep only valid rows
    df = df[df["date"].notna()]
    df = df[df["nav"] > 0]

    return df


def clean_transactions(df):
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )
    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")

    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(
            {
                "sip": "SIP",
                "lumpsum": "Lumpsum",
                "lump sum": "Lumpsum",
                "redemption": "Redemption",
            }
        )
    )

    df["kyc_status"] = (
        df["kyc_status"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    valid_types = ["SIP", "Lumpsum", "Redemption"]
    valid_kyc = ["Verified", "Pending", "Rejected"]

    df = df[df["transaction_date"].notna()]
    df = df[df["amount_inr"] > 0]
    df = df[df["transaction_type"].isin(valid_types)]
    df = df[df["kyc_status"].isin(valid_kyc)]

    return df.drop_duplicates()


def clean_performance(df):
    numeric_columns = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Keep realistic expense ratios; flagging is recorded in a column
    df["expense_ratio_flag"] = ~df["expense_ratio_pct"].between(0.1, 2.5)

    return df.drop_duplicates()


def clean_generic(df):
    return df.drop_duplicates()


def main():
    PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

    files = sorted(RAW_FOLDER.glob("[0-9][0-9]_*.csv"))

    if len(files) != 10:
        print(f"Warning: expected 10 provided CSVs, found {len(files)}.")

    for file_path in files:
        df = pd.read_csv(file_path)

        if file_path.name == "02_nav_history.csv":
            cleaned_df = clean_nav_history(df)
        elif file_path.name == "08_investor_transactions.csv":
            cleaned_df = clean_transactions(df)
        elif file_path.name == "07_scheme_performance.csv":
            cleaned_df = clean_performance(df)
        else:
            cleaned_df = clean_generic(df)

        output_name = file_path.stem + "_cleaned.csv"
        output_path = PROCESSED_FOLDER / output_name
        cleaned_df.to_csv(output_path, index=False)

        print(
            f"{file_path.name}: {len(df)} rows → "
            f"{len(cleaned_df)} rows | saved {output_path.name}"
        )


if __name__ == "__main__":
    main()