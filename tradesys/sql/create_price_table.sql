CREATE TABLE iex_prices
(
    [close] DECIMAL(15, 4),
    [high] DECIMAL(15, 4),
    [low] DECIMAL(15, 4),
    [open] DECIMAL(15, 4),
    [symbol] VARCHAR(20),
    [volume] NUMERIC(20, 0),
    [id] VARCHAR(40),
    [key] VARCHAR(20),
    [subkey] VARCHAR(20),
    [date] DATETIME,
    [updated] NUMERIC(38),
    [changeOverTime] NUMERIC(10),
    [marketChangeOverTime] NUMERIC(10),
    [uClose] DECIMAL(15, 4),
    [uHigh] DECIMAL(15, 4),
    [uLow] DECIMAL(15, 4),
    [uOpen] DECIMAL(15, 4),
    [uVolume] NUMERIC(20, 0),
    [label] VARCHAR(20),
    [change] NUMERIC(38),
    [changePercent] DECIMAL(15, 4)
);
