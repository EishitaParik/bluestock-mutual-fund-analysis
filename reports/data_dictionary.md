# BlueStock Mutual Fund Analytics — Data Dictionary

## Source
All source datasets were provided as CSV files for the BlueStock Mutual Fund Analytics capstone project. Cleaned versions are stored in `data/processed/`.

---

## 01_fund_master_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| amfi_code | Integer | Unique AMFI scheme identifier for a mutual fund. |
| fund_house | Text | Asset Management Company (AMC) managing the fund. |
| scheme_name | Text | Name of the mutual fund scheme. |
| category | Text | Broad scheme category, such as Equity or Debt. |
| sub_category | Text | Specific scheme category, such as Large Cap or Liquid. |
| plan | Text | Fund plan type, such as Direct or Regular. |
| launch_date | Text | Date on which the scheme was launched. |
| benchmark | Text | Market index used to compare fund performance. |
| expense_ratio_pct | Decimal | Annual fund-management expense as a percentage. |
| exit_load_pct | Decimal | Fee charged when units are redeemed early. |
| min_sip_amount | Integer | Minimum amount allowed for a SIP investment. |
| min_lumpsum_amount | Integer | Minimum amount allowed for a one-time investment. |
| fund_manager | Text | Person responsible for managing the scheme. |
| risk_category | Text | Risk classification of the scheme. |
| sebi_category_code | Text | SEBI classification code for the scheme category. |

---

## 02_nav_history_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| amfi_code | Integer | Mutual fund scheme identifier. |
| date | Date | NAV observation date. |
| nav | Decimal | Net Asset Value per unit of the mutual fund. |

---

## 03_aum_by_fund_house_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| date | Date | Reporting date for AUM. |
| fund_house | Text | Asset Management Company name. |
| aum_lakh_crore | Decimal | Assets under management in lakh crore rupees. |
| aum_crore | Integer | Assets under management in crore rupees. |
| num_schemes | Integer | Number of schemes managed by the fund house. |

---

## 04_monthly_sip_inflows_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| month | Text | Reporting month in YYYY-MM format. |
| sip_inflow_crore | Integer | Total SIP inflows in crore rupees. |
| active_sip_accounts_crore | Decimal | Number of active SIP accounts in crore. |
| new_sip_accounts_lakh | Decimal | Number of new SIP accounts in lakh. |
| sip_aum_lakh_crore | Decimal | SIP assets under management in lakh crore rupees. |
| yoy_growth_pct | Decimal | Year-over-year growth percentage in SIP inflows. |

---

## 05_category_inflows_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| month | Text | Reporting month in YYYY-MM format. |
| category | Text | Mutual fund category. |
| net_inflow_crore | Decimal | Net investor inflow or outflow in crore rupees. |

---

## 06_industry_folio_count_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| month | Text | Reporting month in YYYY-MM format. |
| total_folios_crore | Decimal | Total mutual fund folios in crore. |
| equity_folios_crore | Decimal | Equity mutual fund folios in crore. |
| debt_folios_crore | Decimal | Debt mutual fund folios in crore. |
| hybrid_folios_crore | Decimal | Hybrid mutual fund folios in crore. |
| others_folios_crore | Decimal | Other mutual fund folios in crore. |

---

## 07_scheme_performance_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| amfi_code | Integer | Mutual fund scheme identifier. |
| scheme_name | Text | Mutual fund scheme name. |
| fund_house | Text | Asset Management Company name. |
| category | Text | Broad scheme category. |
| plan | Text | Fund plan type. |
| return_1yr_pct | Decimal | One-year annualized return percentage. |
| return_3yr_pct | Decimal | Three-year annualized return percentage. |
| return_5yr_pct | Decimal | Five-year annualized return percentage. |
| benchmark_3yr_pct | Decimal | Benchmark three-year return percentage. |
| alpha | Decimal | Return generated above the benchmark after risk adjustment. |
| beta | Decimal | Sensitivity of fund returns to market movements. |
| sharpe_ratio | Decimal | Risk-adjusted return using total volatility. |
| sortino_ratio | Decimal | Risk-adjusted return using downside volatility. |
| std_dev_ann_pct | Decimal | Annualized standard deviation of returns. |
| max_drawdown_pct | Decimal | Largest peak-to-trough decline percentage. |
| aum_crore | Integer | Scheme assets under management in crore rupees. |
| expense_ratio_pct | Decimal | Annual management expense percentage. |
| morningstar_rating | Integer | Fund rating on a 1–5 scale. |
| risk_grade | Text | Risk grade assigned to the fund. |
| expense_ratio_flag | Boolean | True when expense ratio is outside the expected 0.1%–2.5% range. |

---

## 08_investor_transactions_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| investor_id | Text | Unique identifier for an investor. |
| transaction_date | Date | Date of the investment or redemption transaction. |
| amfi_code | Integer | Mutual fund scheme identifier. |
| transaction_type | Text | Type of transaction: SIP, Lumpsum, or Redemption. |
| amount_inr | Integer | Transaction amount in Indian rupees. |
| state | Text | Investor state. |
| city | Text | Investor city. |
| city_tier | Text | Classification of city by tier. |
| age_group | Text | Investor age-group segment. |
| gender | Text | Investor gender category. |
| annual_income_lakh | Decimal | Annual income in lakh rupees. |
| payment_mode | Text | Payment method used for the transaction. |
| kyc_status | Text | KYC verification status. |

---

## 09_portfolio_holdings_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| amfi_code | Integer | Mutual fund scheme identifier. |
| stock_symbol | Text | Stock-market trading symbol. |
| stock_name | Text | Name of the company held by the fund. |
| sector | Text | Industry sector of the holding. |
| weight_pct | Decimal | Holding weight as a percentage of fund portfolio. |
| market_value_cr | Decimal | Market value of holding in crore rupees. |
| current_price_inr | Decimal | Current market price per share in rupees. |
| portfolio_date | Date | Portfolio disclosure date. |

---

## 10_benchmark_indices_cleaned.csv

| Column | Data Type | Business Definition |
|---|---|---|
| date | Date | Trading date for the benchmark index. |
| index_name | Text | Name of the market benchmark index. |
| close_value | Decimal | Closing value of the benchmark index. |