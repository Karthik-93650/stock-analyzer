📊 Stock Analyzer Dashboard

A simple Flask-based web application that analyzes stock market data and visualizes price trends.
The application allows users to enter stock symbols, choose a time period, and view important statistics along with price charts and moving averages.
This project was built as part of a Python Internship Project Phase and demonstrates how Python can be used for data analysis, visualization, and web development.

📷 Dashboard Preview

(You can replace this later with a full dashboard screenshot.)

🎯 Project Purpose

This project was developed to practice building a data-driven web application using Python and Flask.

It demonstrates how financial data can be collected, analyzed, and visualized in an interactive dashboard.

The project helped strengthen skills in:

API integration

Data analysis using Pandas

Data visualization using Matplotlib

Backend development using Flask

Version control using Git & GitHub

🚀 Features

Analyze real-time stock market data

Compare multiple stocks simultaneously (AAPL, TSLA, MSFT)

Select different time ranges (1 month, 3 months, 6 months, 1 year)

Display key statistics:

Highest price

Lowest price

Average closing price

Moving Average (20-day MA) trend analysis

Trading volume visualization

Display company information (Name, Sector, Market Cap)

Export analyzed stock data as CSV

Clean and responsive Flask dashboard

Error handling for invalid stock symbols

🛠 Technologies Used

Python

Flask

yfinance API

Pandas

Matplotlib

HTML

CSS


# 📁 Project Structure
stock-analyzer
│
├── static
│ ├── style.css
│ └── chart.png
│
├── templates
│ └── index.html
│
├── app.py
├── requirements.txt
└── README.md


---

# ▶️ How to Run the Project

### 1️⃣ Clone the repository


git clone https://github.com/Karthik-93650/stock-analyzer.git


### 2️⃣ Navigate to the project folder


cd stock-analyzer


### 3️⃣ Install required packages


pip install -r requirements.txt


### 4️⃣ Run the Flask application


python app.py


### 5️⃣ Open in your browser


http://127.0.0.1:5000


---

# 📈 How It Works

1. User enters **stock symbol(s)** (example: AAPL, TSLA).
2. User selects a **time period**.
3. The application fetches stock data using **yfinance API**.
4. **Pandas** processes the data and calculates statistics.
5. **Matplotlib** generates charts with moving averages.
6. Results are displayed on the **Flask dashboard**.

---

# 📊 Example Output

The dashboard displays:

- Highest stock price
- Lowest stock price
- Average closing price
- Stock price chart
- Moving average trend
- Trading volume visualization
- Company information
- CSV download option

---

# 📅 Development Progress

## Day 1
- Built a simple stock analyzer using Python
- Fetched stock data using **yfinance**
- Calculated basic statistics

## Day 2
- Created a **Flask web dashboard**
- Added stock price visualization
- Implemented CSV data export
- Improved UI styling

## Day 3
- Added **time period selection**
- Implemented better **error handling**
- Fixed matplotlib backend issues
- Improved dashboard layout

## Day 4
- Added **multi-stock comparison feature**
- Users can analyze multiple stocks at once (AAPL, TSLA, MSFT)
- Improved chart visualization for multiple stock prices

## Day 5
- Added **trading volume visualization**
- Displayed volume bars along with stock price chart
- Improved financial data analysis visualization

## Day 6
- Integrated **company information display**
- Shows company **name, sector, and market capitalization**
- Improved dashboard information panel

---

# 🚀 Future Improvements

Planned enhancements for the next phase:

- Stock news integration
- Advanced technical indicators (**RSI, MACD**)
- Improved UI/UX design
- Deploy the application to cloud (**Render / Railway / AWS**)

---

# 👨‍💻 Author

**Uma Karthik Tanuri**

GitHub:  
https://github.com/Karthik-93650
