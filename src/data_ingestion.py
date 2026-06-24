from pathlib import Path
import pandas as pd

RAW_FOLDER = Path("data/raw")
REPORT_FILE = Path("reports/day1_data_quality_summary.txt")


def main():
    REPORT_FILE.parent.mkdir(exist_ok=True)

    csv_files = sorted(RAW_FOLDER.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/raw.")
        return

    report_lines = [
        "DAY 1 DATA QUALITY SUMMARY",
        f"Total provided CSV files found: {len(csv_files)}",
        ""
    ]

    for file_path in csv_files:
        print("\n" + "=" * 70)
        print(f"FILE: {file_path.name}")
        print("=" * 70)

        try:
            df = pd.read_csv(file_path)

            print("\nShape:", df.shape)
            print("\nData types:")
            print(df.dtypes)
            print("\nFirst 5 rows:")
            print(df.head())

            missing = df.isnull().sum()
            missing = missing[missing > 0]
            duplicates = df.duplicated().sum()

            report_lines.append("=" * 70)
            report_lines.append(f"File: {file_path.name}")
            report_lines.append(f"Shape: {df.shape}")
            report_lines.append(f"Duplicate rows: {duplicates}")

            if missing.empty:
                report_lines.append("Missing values: None")
            else:
                report_lines.append("Missing values:")
                for column, count in missing.items():
                    report_lines.append(f"  - {column}: {count}")

            report_lines.append("Data types:")
            for column, dtype in df.dtypes.items():
                report_lines.append(f"  - {column}: {dtype}")
            report_lines.append("")

        except Exception as error:
            print(f"Could not read {file_path.name}: {error}")
            report_lines.append(f"ERROR reading {file_path.name}: {error}\n")

    fund_master_file = RAW_FOLDER / "01_fund_master.csv"
    nav_history_file = RAW_FOLDER / "02_nav_history.csv"

    if fund_master_file.exists() and nav_history_file.exists():
        fund_master = pd.read_csv(fund_master_file)
        nav_history = pd.read_csv(nav_history_file)

        print("\n" + "=" * 70)
        print("FUND MASTER EXPLORATION")
        print("=" * 70)

        report_lines.append("=" * 70)
        report_lines.append("FUND MASTER EXPLORATION")

        for column in ["fund_house", "category", "sub_category", "risk_category"]:
            if column in fund_master.columns:
                values = sorted(fund_master[column].dropna().unique())
                print(f"\nUnique {column}:")
                print(values)
                report_lines.append(f"Unique {column}: {values}")

        if "amfi_code" in fund_master.columns and "amfi_code" in nav_history.columns:
            master_codes = set(fund_master["amfi_code"].astype(str))
            nav_codes = set(nav_history["amfi_code"].astype(str))
            missing_codes = master_codes - nav_codes

            print("\nAMFI CODE VALIDATION")
            print(f"Fund-master codes: {len(master_codes)}")
            print(f"NAV-history codes: {len(nav_codes)}")
            print(f"Codes missing from NAV history: {len(missing_codes)}")

            report_lines.append("")
            report_lines.append("AMFI CODE VALIDATION")
            report_lines.append(f"Fund-master codes: {len(master_codes)}")
            report_lines.append(f"NAV-history codes: {len(nav_codes)}")
            report_lines.append(f"Codes missing from NAV history: {len(missing_codes)}")

            if missing_codes:
                report_lines.append(f"Missing codes: {sorted(missing_codes)}")
            else:
                report_lines.append("All fund_master AMFI codes exist in nav_history.")

    REPORT_FILE.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nSaved report: {REPORT_FILE}")


if __name__ == "__main__":
    main()

