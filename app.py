import yfinance as yf


def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1y")
    return data

def show_summary(data):
    highest = data["High"].max()
    lowest = data["Low"].min()
    average = data["Close"].mean()
    print("\nStock Summary")
    print("-------------------")
    print("Highest Price :", round(highest, 2))
    print("Lowest Price  :", round(lowest, 2))
    print("Average Close :", round(average, 2))

def main():
    print("📊 Simple Stock Analyzer")
    symbol = input("Enter stock symbol (example: AAPL): ").upper()
    data = get_stock_data(symbol)
    if data.empty:
        print("No data found. Try another symbol.")
        return
    show_summary(data)


if __name__ == "__main__":
    main()