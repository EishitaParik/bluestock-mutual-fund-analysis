import pandas as pd

# Load data
performance = pd.read_csv("../data/raw/07_scheme_performance.csv")

# Get user input
risk = input("Enter Risk Appetite (Low / Moderate / High): ")

# Recommend funds
recommended = (
    performance[
        performance["risk_grade"].str.lower() == risk.lower()
    ]
    .sort_values("sharpe_ratio", ascending=False)
    .head(3)
)

print("\nTop 3 Recommended Funds\n")

print(
    recommended[
        [
            "scheme_name",
            "risk_grade",
            "sharpe_ratio",
            "return_3yr_pct",
        ]
    ]
)