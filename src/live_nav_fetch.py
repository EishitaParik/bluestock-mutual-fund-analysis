from pathlib import Path
import time

import pandas as pd
import requests

RAW_FOLDER = Path("data/raw")

SCHEMES = {
    "hdfc_top_100_direct": "125497",
    "sbi_bluechip": "119551",
    "icici_bluechip": "120503",
    "nippon_large_cap": "118632",
    "axis_bluechip": "119092",
    "kotak_bluechip": "120841",
}


def fetch_nav(scheme_name, amfi_code):
    url = f"https://api.mfapi.in/mf/{amfi_code}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    api_response = response.json()
    metadata = api_response.get("meta", {})
    nav_data = api_response.get("data", [])

    df = pd.DataFrame(nav_data)

    if df.empty:
        print(f"No NAV data found for {scheme_name}.")
        return None

    df["amfi_code"] = amfi_code
    df["scheme_name"] = metadata.get("scheme_name", scheme_name)
    df["fund_house"] = metadata.get("fund_house", "Unknown")
    df["scheme_category"] = metadata.get("scheme_category", "Unknown")
    df["scheme_type"] = metadata.get("scheme_type", "Unknown")

    return df


def main():
    RAW_FOLDER.mkdir(parents=True, exist_ok=True)
    all_schemes = []

    for scheme_name, amfi_code in SCHEMES.items():
        print(f"Fetching {scheme_name}...")

        try:
            df = fetch_nav(scheme_name, amfi_code)

            if df is not None:
                output_path = RAW_FOLDER / f"live_nav_{scheme_name}.csv"
                df.to_csv(output_path, index=False)

                all_schemes.append(df)
                print(f"Saved: {output_path}")

        except requests.RequestException as error:
            print(f"Could not fetch {scheme_name}: {error}")

        time.sleep(1)

    if all_schemes:
        combined_df = pd.concat(all_schemes, ignore_index=True)
        combined_path = RAW_FOLDER / "live_nav_all_schemes.csv"
        combined_df.to_csv(combined_path, index=False)
        print(f"\nSaved combined file: {combined_path}")


if __name__ == "__main__":
    main()