CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_name TEXT,
    website TEXT
);

CREATE TABLE profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);

CREATE TABLE balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    total_liabilities REAL,
    total_assets REAL,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);