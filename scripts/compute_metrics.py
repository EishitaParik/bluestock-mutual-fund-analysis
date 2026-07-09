import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from scipy.stats import linregress

plt.style.use("ggplot")

def calculate_cagr(start_nav, end_nav, years):
    return ((end_nav / start_nav) ** (1 / years)) - 1

sharpe_results = []

for fund in nav_df["amfi_code"].unique():

    fund_returns = nav_df[
        nav_df["amfi_code"] == fund
    ]["daily_return"].dropna()

    if len(fund_returns) == 0:
        continue

    annual_return = fund_returns.mean() * 252
    annual_volatility = fund_returns.std() * np.sqrt(252)

    sharpe = (annual_return - risk_free_rate) / annual_volatility

    sharpe_results.append({
        "amfi_code": fund,
        "Annual Return": annual_return,
        "Annual Volatility": annual_volatility,
        "Sharpe Ratio": sharpe
    })

    sharpe_df = pd.DataFrame(sharpe_results)

sharpe_df = sharpe_df.sort_values(
    by="Sharpe Ratio",
    ascending=False
)

sharpe_df.head(10)


slope, intercept, r_value, p_value, std_err = linregress(
    merged["benchmark_return"],
    merged["daily_return"]
)

alpha = intercept * 252
beta = slope

print("Alpha:", alpha)
print("Beta:", beta)

alpha_beta_results = []


for fund in nav_df["amfi_code"].unique():

    fund_df = nav_df[
        nav_df["amfi_code"] == fund
    ][["date", "daily_return"]].copy()

    fund_df["date"] = pd.to_datetime(fund_df["date"])

    merged = pd.merge(
        fund_df,
        nifty100[["date", "benchmark_return"]],
        on="date",
        how="inner"
    )

    merged = merged.dropna()

    if len(merged) < 30:
        continue

    slope, intercept, r_value, p_value, std_err = linregress(
        merged["benchmark_return"],
        merged["daily_return"]
    )

    alpha_beta_results.append({
        "amfi_code": fund,
        "Alpha": intercept * 252,
        "Beta": slope,
        "R_squared": r_value**2
    })


    alpha_beta_df = pd.DataFrame(alpha_beta_results)


    alpha_beta_df.head()

    alpha_beta_df = alpha_beta_df.sort_values(
    by="Alpha",
    ascending=False
)

alpha_beta_df.head(10)

alpha_beta_df.to_csv("../reports/alpha_beta.csv", index=False)

drawdown_results = []

for fund in nav_df["amfi_code"].unique():

    fund_df = nav_df[
        nav_df["amfi_code"] == fund
    ].copy()

    fund_df = fund_df.sort_values("date")

    # Running maximum NAV
    fund_df["running_max"] = fund_df["nav"].cummax()

    # Drawdown
    fund_df["drawdown"] = (
        fund_df["nav"] / fund_df["running_max"]
    ) - 1

    # Worst drawdown
    max_dd = fund_df["drawdown"].min()

    # Date when it happened
    worst_row = fund_df.loc[
        fund_df["drawdown"].idxmin()
    ]

    drawdown_results.append({
        "amfi_code": fund,
        "Maximum Drawdown": max_dd,
        "Worst Date": worst_row["date"]
    })

    drawdown_df = pd.DataFrame(drawdown_results)

    drawdown_df = drawdown_df.sort_values(
    by="Maximum Drawdown"
)

drawdown_df.head(10)

plt.figure(figsize=(12,6))

sns.barplot(
    data=drawdown_df.head(10),
    x="Maximum Drawdown",
    y="amfi_code",
    palette="Reds_r"
)

plt.title("Top 10 Worst Maximum Drawdowns")
plt.xlabel("Maximum Drawdown")
plt.ylabel("AMFI Code")

plt.tight_layout()
plt.show()

drawdown_df.to_csv(
    "../reports/maximum_drawdown.csv",
    index=False
)

scorecard["CAGR Rank"] = scorecard["CAGR_3Y"].rank(ascending=False)

scorecard["Sharpe Rank"] = scorecard["Sharpe Ratio"].rank(ascending=False)

scorecard["Alpha Rank"] = scorecard["Alpha"].rank(ascending=False)

scorecard["Expense Rank"] = scorecard["expense_ratio_pct"].rank(ascending=True)

scorecard["Drawdown Rank"] = scorecard["Maximum Drawdown"].rank(ascending=False)


scorecard["Weighted Score"] = (
      0.30 * scorecard["CAGR Rank"]
    + 0.25 * scorecard["Sharpe Rank"]
    + 0.20 * scorecard["Alpha Rank"]
    + 0.15 * scorecard["Expense Rank"]
    + 0.10 * scorecard["Drawdown Rank"]
)


scorecard["Fund Score"] = (
    (scorecard["Weighted Score"].max() - scorecard["Weighted Score"])
    /
    (scorecard["Weighted Score"].max() - scorecard["Weighted Score"].min())
) * 100


scorecard = scorecard.sort_values(
    by="Fund Score",
    ascending=False
)

scorecard.head(10)


scorecard.to_csv(
    "../reports/fund_scorecard.csv",
    index=False
)

benchmark_df["date"] = pd.to_datetime(benchmark_df["date"])

nifty50 = benchmark_df[
    benchmark_df["index_name"] == "NIFTY50"
].copy()

nifty100 = benchmark_df[
    benchmark_df["index_name"] == "NIFTY100"
].copy()

nifty50 = nifty50.sort_values("date")
nifty100 = nifty100.sort_values("date")


tracking_df = pd.DataFrame(tracking_results)

tracking_df

tracking_df.to_csv(
    "../reports/tracking_error.csv",
    index=False
)

best_fund = top5_funds[0]

best_df = nav_df[
    nav_df["amfi_code"] == best_fund
].copy()

comparison = pd.merge(
    best_df[["date", "nav"]],
    nifty100[["date", "close_value"]],
    on="date"
)




var_cvar = []

for code, group in nav.groupby('amfi_code'):
    returns = group['daily_return'].dropna()

    if len(returns) > 0:
        var_95 = returns.quantile(0.05)
        cvar_95 = returns[returns <= var_95].mean()

        var_cvar.append({
            'amfi_code': code,
            'VaR_95': var_95,
            'CVaR_95': cvar_95
        })

var_cvar_df = pd.DataFrame(var_cvar)

var_cvar_df.head()

var_cvar_df.to_csv("var_cvar_report.csv", index=False)



cohort_analysis = (
    avg_sip.merge(total_invested, on="cohort_year")
           .merge(
               top_funds[["cohort_year", "scheme_name"]],
               on="cohort_year"
           )
)

cohort_analysis


cohort_analysis.to_csv(
    "cohort_analysis.csv",
    index=False
)


sip_count = sip.groupby("investor_id").size()

eligible = sip_count[sip_count >= 6].index

sip6 = sip[sip["investor_id"].isin(eligible)]

continuity = (
    sip6.groupby("investor_id")["gap_days"]
        .mean()
        .reset_index()
)

continuity.rename(columns={"gap_days":"avg_gap_days"}, inplace=True)

continuity["status"] = continuity["avg_gap_days"].apply(
    lambda x: "At Risk" if x > 35 else "Regular"
)

continuity.head()

continuity.to_csv("sip_continuity_report.csv", index=False)



hhi = (
    holdings
    .groupby("amfi_code")["weight_pct"]
    .apply(lambda x: ((x / 100) ** 2).sum())
    .reset_index(name="HHI")
)

hhi.head()

hhi = hhi.merge(
    funds[["amfi_code", "scheme_name"]],
    on="amfi_code",
    how="left"
)

hhi.head()


hhi = hhi.sort_values("HHI", ascending=False)

hhi.head(10)

hhi.to_csv("sector_hhi_report.csv", index=False)


hhi = (
    holdings
    .groupby("amfi_code")["weight_pct"]
    .apply(lambda x: ((x / 100) ** 2).sum())
    .reset_index(name="HHI")
)

hhi = hhi.merge(
    funds[["amfi_code", "scheme_name"]],
    on="amfi_code",
    how="left"
)

hhi = hhi.sort_values("HHI", ascending=False)

hhi.head(10)