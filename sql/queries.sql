-- 1. Top 5 funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;


-- 2. Average NAV per month
SELECT
    substr(date, 1, 7) AS month,
    ROUND(AVG(nav), 2) AS average_nav
FROM fact_nav
GROUP BY substr(date, 1, 7)
ORDER BY month;


-- 3. SIP inflow year-over-year growth
SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM fact_sip_inflows
ORDER BY month;


-- 4. Number of transactions by state
SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;


-- 5. Funds with expense ratio below 1%
SELECT
    scheme_name,
    fund_house,
    category,
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;


-- 6. Top 5 fund houses by AUM
SELECT
    fund_house,
    ROUND(MAX(aum_crore), 2) AS latest_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY latest_aum_crore DESC
LIMIT 5;


-- 7. Transaction type summary
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;


-- 8. Best 5 funds by 3-year return
SELECT
    scheme_name,
    fund_house,
    return_3yr_pct,
    benchmark_3yr_pct,
    alpha
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;


-- 9. Average NAV by fund
SELECT
    f.scheme_name,
    ROUND(AVG(n.nav), 2) AS average_nav
FROM fact_nav AS n
JOIN dim_fund AS f
    ON n.amfi_code = f.amfi_code
GROUP BY f.scheme_name
ORDER BY average_nav DESC;


-- 10. KYC status summary
SELECT
    kyc_status,
    COUNT(*) AS investor_transactions
FROM fact_transactions
GROUP BY kyc_status
ORDER BY investor_transactions DESC;