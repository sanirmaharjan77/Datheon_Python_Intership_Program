"""
Stock Portfolio Performance Tracker
Run:  python portfolio.py
(Optional, for live prices: pip install yfinance)
"""

import csv

# ======================================================================
# STEP 1: EDIT THIS - put your stocks here. No typing needed when running.
#         Format:  "TICKER": {"buy_price": price you paid, "shares": how many}
# ======================================================================
PORTFOLIO = {
    "AAPL": {"buy_price": 150.00, "shares": 10},
    "MSFT": {"buy_price": 300.00, "shares": 5},
    "NVDA": {"buy_price": 100.00, "shares": 8},
}

# Used only if live prices can't be fetched (no internet / yfinance not installed)
BACKUP_PRICES = {
    "AAPL": 230.00,
    "MSFT": 420.00,
    "NVDA": 140.00,
}

TICKER_FILE = "sp500_companies.csv"
OUTPUT_FILE = "portfolio_summary.csv"


def load_company_names(path):
    """Read company names from the S&P 500 CSV."""
    names = {}
    try:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                names[row["Symbol"].strip().upper()] = row["Security"].strip()
    except FileNotFoundError:
        print(f"Note: '{path}' not found, company names will be blank.")
    return names


def get_price(symbol):
    """Live price from yfinance, else backup price, else None."""
    try:
        import yfinance as yf
        price = yf.Ticker(symbol.replace(".", "-")).fast_info["last_price"]
        if price and price > 0:
            return float(price), "live"
    except Exception:
        pass
    if symbol in BACKUP_PRICES:
        return BACKUP_PRICES[symbol], "backup"
    return None, None


def main():
    names = load_company_names(TICKER_FILE)
    rows = []

    print("\n" + "=" * 86)
    print(f"{'PORTFOLIO PERFORMANCE':^86}")
    print("=" * 86)
    print(f"{'Symbol':<8}{'Company':<20}{'Shares':>7}{'Buy $':>10}{'Now $':>10}"
          f"{'Invested':>12}{'Value':>12}{'P/L %':>9}")
    print("-" * 86)

    for symbol, pos in PORTFOLIO.items():
        symbol = symbol.upper()
        price, source = get_price(symbol)
        if price is None:
            print(f"{symbol:<8}-- no price available, skipped --")
            continue

        invested = pos["buy_price"] * pos["shares"]
        value = price * pos["shares"]
        gain = value - invested
        pct = gain / invested * 100

        print(f"{symbol:<8}{names.get(symbol, '')[:18]:<20}{pos['shares']:>7}"
              f"{pos['buy_price']:>10,.2f}{price:>10,.2f}"
              f"{invested:>12,.2f}{value:>12,.2f}{pct:>+8.2f}%")
        rows.append([symbol, names.get(symbol, ""), pos["shares"], pos["buy_price"],
                     round(price, 2), round(invested, 2), round(value, 2),
                     round(gain, 2), round(pct, 2), source])

    total_inv = sum(r[5] for r in rows)
    total_val = sum(r[6] for r in rows)
    total_gain = total_val - total_inv
    total_pct = total_gain / total_inv * 100 if total_inv else 0

    print("-" * 86)
    print(f"Total invested : ${total_inv:,.2f}")
    print(f"Current value  : ${total_val:,.2f}")
    print(f"Total gain/loss: ${total_gain:+,.2f} ({total_pct:+.2f}%)")
    print("=" * 86)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Company", "Shares", "Buy Price", "Current Price",
                         "Invested", "Market Value", "Gain/Loss ($)", "Gain/Loss (%)",
                         "Price Source"])
        writer.writerows(rows)
        writer.writerow(["TOTAL", "", "", "", "", round(total_inv, 2), round(total_val, 2),
                         round(total_gain, 2), round(total_pct, 2), ""])
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
