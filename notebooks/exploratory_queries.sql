SELECT COUNT(*) FROM companies;

SELECT COUNT(*) FROM profitandloss;

SELECT COUNT(*) FROM balancesheet;

SELECT COUNT(*) FROM cashflow;

SELECT company_id, MAX(sales)
FROM profitandloss
GROUP BY company_id
LIMIT 10;

SELECT company_id, MAX(net_profit)
FROM profitandloss
GROUP BY company_id
LIMIT 10;

SELECT company_id, AVG(opm_percentage)
FROM profitandloss
GROUP BY company_id
LIMIT 10;

SELECT company_id, COUNT(*)
FROM profitandloss
GROUP BY company_id;

SELECT *
FROM companies
LIMIT 5;

SELECT *
FROM stock_prices
LIMIT 5;