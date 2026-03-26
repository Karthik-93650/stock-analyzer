# 📊 Stock Analyzer Dashboard

A simple **Flask-based web application** that analyzes stock market data and visualizes price trends.

The application allows users to enter a stock symbol, choose a time period, and view important statistics along with a price chart and moving average.

This project was built as part of a **Python Internship Project Phase** and demonstrates how Python can be used for **data analysis, visualization, and web development**.

---

# 🚀 Features

- User authentication (Login / Signup)
- Analyze real-time stock market data
- Multi-stock comparison
- Time period selection
- Stock price + volume charts
- Company information (name, sector, market cap)
- Search history tracking
- Watchlist management
- CSV data export

---

# 🛠 Technologies Used

* **Python**
* **Flask**
* **yfinance**
* **Pandas**
* **Matplotlib**
* **HTML**
* **CSS**

---

# 📁 Project Structure

```
stock-analyzer
│
├── static
│   ├── style.css
│   └── chart.png
│
├── templates
│   └── index.html
│
├── app.py
├── requirements.txt
└── README.md
```

---

# ▶️ How to Run the Project

### 1️⃣ Clone the repository

```
git clone https://github.com/Karthik-93650/stock-analyzer.git
```

### 2️⃣ Navigate to the project folder

```
cd stock-analyzer
```

### 3️⃣ Install required packages

```
pip install -r requirements.txt
```

### 4️⃣ Run the Flask application

```
python app.py
```

### 5️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

# 📈 How It Works

1. User enters a **stock symbol** (example: AAPL, TSLA).
2. User selects a **time period**.
3. The application fetches stock data using **yfinance**.
4. **Pandas** processes the data and calculates statistics.
5. **Matplotlib** generates a price chart with moving average.
6. Results are displayed on the dashboard.

---

# 📊 Example Output

The dashboard shows:

* Highest price
* Lowest price
* Average price
* Stock price chart
* Moving average line
* CSV download option

---

# 📅 Development Progress

### Day 1

* Built a simple stock analyzer using Python
* Fetched stock data using yfinance
* Calculated basic statistics

### Day 2

* Created a Flask web dashboard
* Added stock price visualization
* Implemented CSV data export
* Improved UI styling

### Day 3

* Added time period selection
* Implemented better error handling
* Fixed matplotlib backend issues
* Improved dashboard layout

---

# 🎯 Future Improvements

Planned enhancements for the next phase:

* Multi-stock comparison
* Volume chart visualization
* Stock news integration
* UI improvements

---

# 👨‍💻 Author

**Uma Karthik Tanuri**

GitHub:
https://github.com/Karthik-93650
