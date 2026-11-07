# Datheon Python Programming Internship

Python programming internship tasks.

## Task 1: Hangman Word Guessing Game (Console)

A terminal-based Hangman game written in Python 3.

### Features
- Random secret word chosen from `words.txt`
- ASCII gallows art that updates after each wrong guess
- 6 mistakes allowed; repeated guesses don't cost a life
- Victory and defeat screens that reveal the answer
- Play-again option

### How to run
1. Keep `Hangman1.py` and `words.txt` in the same folder.
2. Run: `python3 Hangman1.py`

### Tools
Python 3, VS Code, Git/GitHub


# Task 2

# Stock Portfolio Performance Tracker

A simple Python program that calculates the value of your stock portfolio,
shows the percentage gain or loss for each stock, and saves the results to a CSV file.

## Files

| File | Purpose |
|------|---------|
| `portfolio.py` | The main program |
| `sp500_companies.csv` | S&P 500 dataset (used for company names) |
| `portfolio_summary.csv` | Output file, created when you run the program |

## Requirements

- Python 3
- Optional, for live prices: `yfinance`

```
pip install yfinance
```

Without yfinance the program still works. It uses the backup prices
written in the file.

## How to Use

1. Put `portfolio.py` and `sp500_companies.csv` in the same folder.
2. Open `portfolio.py` and edit the `PORTFOLIO` section with your stocks:

```python
PORTFOLIO = {
    "AAPL": {"buy_price": 150.00, "shares": 10},
    "MSFT": {"buy_price": 300.00, "shares": 5},
}
```

3. (Optional) Edit `BACKUP_PRICES` with current prices. These are used
   only if live prices cannot be fetched.
4. Run the program:

```
python portfolio.py
```

## What It Does

1. Stores your holdings in a dictionary.
2. Looks up each stock's current price (live via yfinance, otherwise backup).
3. Calculates:
   - Total invested capital
   - Current market value
   - Gain/loss in dollars and percent, per stock and overall
4. Prints a formatted table in the console.
5. Saves the results to `portfolio_summary.csv` using Python's built-in `csv` module.

## Example Output

```
Symbol  Company       Shares     Buy $     Now $    Invested       Value    P/L %
AAPL    Apple Inc.        10    150.00    230.00    1,500.00    2,300.00  +53.33%
MSFT    Microsoft          5    300.00    420.00    1,500.00    2,100.00  +40.00%

Total invested : $3,000.00
Current value  : $4,400.00
Total gain/loss: +$1,400.00 (+46.67%)
```

## Output File

`portfolio_summary.csv` contains one row per stock plus a TOTAL row, with these columns:
Symbol, Company, Shares, Buy Price, Current Price, Invested, Market Value,
Gain/Loss ($), Gain/Loss (%), Price Source (live or backup).

## Notes

- Stock tickers must match the S&P 500 symbols (e.g., `AAPL`, `MSFT`, `NVDA`).
- Running the program again overwrites `portfolio_summary.csv`.
- Prices are for educational use only and are not financial advice.

## Tools Used

Python 3, csv module, file I/O, yfinance (optional)