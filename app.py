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

    if request.method == "POST":
        symbol = request.form["symbol"].upper().strip()
        period = request.form.get("period", "6mo")

        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)

            if df.empty:
                error = "Invalid stock symbol or no data found."
            else:
                df["MA20"] = df["Close"].rolling(window=20).mean()

                stats = {
                    "highest": round(df["High"].max(), 2),
                    "lowest": round(df["Low"].min(), 2),
                    "average": round(df["Close"].mean(), 2)
                }

                df.to_csv("stock_data.csv")

                plt.figure(figsize=(8,4))
                plt.plot(df["Close"], label="Close Price")
                plt.plot(df["MA20"], label="20 Day MA")
                plt.legend()
                plt.title(f"{symbol} Stock Price ({period})")
                plt.tight_layout()
                plt.savefig("static/chart.png")
                plt.close()

                data = True

        except Exception as e:
            print(e)
            error = "Something went wrong. Please try again."

    return render_template("index.html",stats=stats,data=data,error=error,symbol=symbol,period=period)


@app.route("/download")
def download():
    if os.path.exists("stock_data.csv"):
        return send_file("stock_data.csv", as_attachment=True)
    return "No file available to download."


if __name__ == "__main__":
    app.run(debug=True)