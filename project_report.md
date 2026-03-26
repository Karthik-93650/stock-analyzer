# Final Project Report: Stock Analysis Dashboard

## 1. Project Overview
The **Stock Analysis Dashboard** is a full-stack Python web application designed to allow users to analyze stock market trends, manage a portfolio, and allow administrators to control the available stocks in the platform. The project is fully completed and all files have been reviewed and standardized.

## 2. Codebase Review & "Humanized Basic Code" Status
As requested, the entire codebase has been thoroughly reviewed to ensure it uses **basic, human-readable logic** suitable for an interview presentation and easy explanation:
- **Error Handling**: All `try-except` blocks uniformly include `else` blocks for consistent, basic conditional flow.
- **Data Structures and Loops**: Advanced list comprehensions and complex one-line map/filter operations were expanded into standard [for](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/app.py#23-33) loops.
- **Debugging**: Advanced logging libraries/configurations have been entirely replaced with basic `print()` statements.
- **Structure**: The Flask routing and function definitions avoid overly nested decorators or class-based views in favor of basic function-based routing.

## 3. Technology Stack
- **Backend:** Python + Flask
- **Data Fetching:** `yfinance` API module
- **Data Processing:** `pandas` (using basic DataFrame operations)
- **Database:** MySQL (interfaced via `mysql-connector-python`)
- **Data Visualization:** `matplotlib` (rendered as backend static images)
- **Frontend:** HTML5, standard Jinja2 templating, and vanilla CSS (`style.css`).

## 4. Features Implemented

### For Regular Users:
- **Authentication**: Signup and Login with plain hashed passwords.
- **Dashboard/Screener**: Analyze stocks over variable timeframes (1M, 3M, 6M, 1Y, MAX).
- **History & Watchlist**: Save analyzed stock history and manage a personal watchlist.
- **Buy Stocks**: Users can view the admin-approved stock list and perform mock "buying" based on real-time prices.
- **Portfolio Management**: Auto-calculates current return on investment (ROI), current value, and profit/loss.
- **Data Export**: Provides CSV downloads for local analysis.

### For Administrators:
- **Admin Dashboard**: Special interface for users designated with the [admin](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/app.py#397-425) role.
- **Stock Management**: Ability to query the Yahoo Finance API to vet and add stock symbols into the system's "Available Stocks" list. Admin can also remove stocks.

## 5. File Structure
- [app.py](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/app.py): The Main Flask Application containing basic routes and logic.
- [database.sql](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/database.sql): Basic SQL commands manually creating required tables (`users`, [history](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/app.py#286-305), [watchlist](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/app.py#337-356), [available_stocks](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/app.py#484-512), [portfolio](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/app.py#543-584)).
- [requirements.txt](file:///c:/Users/LENOVO/Desktop/PROJECTS/stock-analysis-dashboard/requirements.txt): Project dependencies (Flask, pandas, yfinance, matplotlib, mysql-connector-python).
- `templates/`: Contains all basic raw HTML and Jinja template logic.
- `static/`: Contains generated chart imagery and basic CSS files.

## Conclusion
The project is structurally sound, logically basic, and thoroughly commented where necessary. It is fully ready for deployment or academic presentation.
