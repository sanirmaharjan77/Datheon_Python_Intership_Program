

import csv
import os
from datetime import datetime

TICKER_FILE = "sp500_companies.csv"
OUTPUT_FILE = "portfolio_summary.csv"

CSV_FIELDS = [
    "Timestamp", "Symbol", "Company", "Shares", "Buy Price",
    "Current Price", "Invested", "Market Value", "Gain/Loss ($)", "Gain/Loss (%)",
]


# ---------- Data loading ----------
def load_tickers(path):
    """Return {symbol: company_name} from the S&P 500 CSV."""
    tickers = {}
    try:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                tickers[row["Symbol"].strip().upper()] = row["Security"].strip()
    except FileNotFoundError:
        print(f"[!] '{path}' not found - ticker validation disabled.")
    return tickers


def fetch_price(symbol):
    """Try to get the latest price from yfinance. Returns float or None."""
    try:
        import yfinance as yf
        yf_symbol = symbol.replace(".", "-")  # e.g. BRK.B -> BRK-B
        price = yf.Ticker(yf_symbol).fast_info["last_price"]
        if price and price > 0:
            return float(price)
    except Exception:
        pass
    return None


# ---------- Input helpers ----------
def ask_float(prompt, minimum_exclusive=0.0):
    while True:
        try:
            value = float(input(prompt).replace(",", "").replace("$", ""))
            if value > minimum_exclusive:
                return value
            print(f"  Value must be greater than {minimum_exclusive}.")
        except ValueError:
            print("  Please enter a valid number.")


def collect_positions(tickers):
    """Collect positions into a dict: {symbol: {'shares': x, 'buy_price': y}}."""
    portfolio = {}
    print("\nEnter your holdings. Type 'done' as the ticker when finished.\n")
    while True:
        symbol = input("Ticker symbol: ").strip().upper()
        if symbol == "DONE":
            if portfolio:
                break
            print("  Add at least one holding first.")
            continue
        if not symbol:
            continue
        if tickers and symbol not in tickers:
            print(f"  '{symbol}' is not in the S&P 500 list. Try again.")
            continue

        buy_price = ask_float("  Buy price per share ($): ")
        shares = ask_float("  Number of shares: ")

        if symbol in portfolio:  # merge with weighted-average cost
            old = portfolio[symbol]
            total_shares = old["shares"] + shares
            avg = (old["shares"] * old["buy_price"] + shares * buy_price) / total_shares
            portfolio[symbol] = {"shares": total_shares, "buy_price": avg}
            print(f"  Merged with existing position (avg cost ${avg:,.2f}).")
        else:
            portfolio[symbol] = {"shares": shares, "buy_price": buy_price}
        print(f"  Added {symbol}.\n")
    return portfolio


# ---------- Calculations ----------
def analyze(portfolio, tickers):
    results = []
    for symbol, pos in portfolio.items():
        price = fetch_price(symbol)
        if price is None:
            print(f"[!] Could not fetch live price for {symbol}.")
            price = ask_float(f"    Enter current price for {symbol} ($): ")

        invested = pos["shares"] * pos["buy_price"]
        value = pos["shares"] * price
        gain = value - invested
        pct = gain / invested * 100

        results.append({
            "Symbol": symbol,
            "Company": tickers.get(symbol, "N/A"),
            "Shares": pos["shares"],
            "Buy Price": pos["buy_price"],
            "Current Price": price,
            "Invested": invested,
            "Market Value": value,
            "Gain/Loss ($)": gain,
            "Gain/Loss (%)": pct,
        })
    return results


# ---------- Output ----------
def print_report(results):
    line = "=" * 98
    print(f"\n{line}")
    print(f"{'PORTFOLIO PERFORMANCE':^98}")
    print(line)
    print(f"{'Symbol':<8}{'Company':<22}{'Shares':>9}{'Buy $':>11}{'Now $':>11}"
          f"{'Invested':>13}{'Value':>13}{'P/L %':>10}")
    print("-" * 98)
    for r in results:
        print(f"{r['Symbol']:<8}{r['Company'][:20]:<22}{r['Shares']:>9,.2f}"
              f"{r['Buy Price']:>11,.2f}{r['Current Price']:>11,.2f}"
              f"{r['Invested']:>13,.2f}{r['Market Value']:>13,.2f}"
              f"{r['Gain/Loss (%)']:>+9.2f}%")
    print("-" * 98)

    total_inv = sum(r["Invested"] for r in results)
    total_val = sum(r["Market Value"] for r in results)
    total_gain = total_val - total_inv
    total_pct = total_gain / total_inv * 100

    print(f"{'Total invested capital:':<30}${total_inv:>15,.2f}")
    print(f"{'Total market value:':<30}${total_val:>15,.2f}")
    print(f"{'Total gain/loss:':<30}${total_gain:>+15,.2f}  ({total_pct:+.2f}%)")
    print(line)
    return total_inv, total_val, total_gain, total_pct


def save_to_csv(results, totals, path):
    """Append this run to the log (header written only if file is new)."""
    total_inv, total_val, total_gain, total_pct = totals
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_new = not os.path.exists(path) or os.path.getsize(path) == 0

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if is_new:
            writer.writeheader()
        for r in results:
            row = {"Timestamp": stamp}
            for key, val in r.items():
                row[key] = round(val, 2) if isinstance(val, float) else val
            writer.writerow(row)
        writer.writerow({
            "Timestamp": stamp, "Symbol": "TOTAL", "Company": "Portfolio",
            "Invested": round(total_inv, 2), "Market Value": round(total_val, 2),
            "Gain/Loss ($)": round(total_gain, 2), "Gain/Loss (%)": round(total_pct, 2),
        })
    print(f"\nSummary saved to '{path}'.")


def main():
    print("=== Stock Portfolio Performance Tracker ===")
    tickers = load_tickers(TICKER_FILE)
    portfolio = collect_positions(tickers)
    results = analyze(portfolio, tickers)
    totals = print_report(results)
    save_to_csv(results, totals, OUTPUT_FILE)


if __name__ == "__main__":
    main()