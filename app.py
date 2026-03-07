from flask import Flask, render_template, request, send_file
import yfinance as yf
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

plt.style.use("ggplot")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    stats = {}
    error = None
    symbol = ""
    period = "6mo"

    company = None
    sector = None
    marketcap = None

    if request.method == "POST":
        symbol = request.form["symbol"].upper().strip()
        period = request.form.get("period", "6mo")

        symbols = symbol.split(",")

        try:
            plt.figure(figsize=(10,5))

            for s in symbols:
                s = s.strip()

                stock = yf.Ticker(s)
                df = stock.history(period=period)

                if df.empty:
                    continue

                # moving average
                df["MA20"] = df["Close"].rolling(window=20).mean()

                # plot price
                plt.plot(df["Close"], label=f"{s} Close")

                # plot volume
                plt.bar(df.index, df["Volume"], alpha=0.15)

                # calculate stats for first stock
                if not stats:
                    stats = {
                        "highest": round(df["High"].max(), 2),
                        "lowest": round(df["Low"].min(), 2),
                        "average": round(df["Close"].mean(), 2)
                    }

                    # company information
                    info = stock.info
                    company = info.get("longName", s)
                    sector = info.get("sector", "N/A")
                    marketcap = info.get("marketCap", "N/A")

                # save csv
                df.to_csv("stock_data.csv")

            if stats:
                plt.legend()
                plt.title(f"Stock Comparison ({period})")
                plt.tight_layout()
                plt.savefig("static/chart.png")
                plt.close()

                data = True
            else:
                error = "Invalid stock symbol or no data found."

        except Exception as e:
            print(e)
            error = "Something went wrong. Please try again."

    return render_template(
        "index.html",
        stats=stats,
        data=data,
        error=error,
        symbol=symbol,
        period=period,
        company=company,
        sector=sector,
        marketcap=marketcap
    )


@app.route("/download")
def download():
    if os.path.exists("stock_data.csv"):
        return send_file("stock_data.csv", as_attachment=True)
    return "No file available to download."


if __name__ == "__main__":
    app.run(debug=True)