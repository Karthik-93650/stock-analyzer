from flask import Flask, render_template, request, flash, redirect, url_for, send_file, session
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import (connection)
import os
import time
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

mydb = connection.MySQLConnection(user='root', host='localhost', password='admin', database='stock')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(BASE_DIR)

STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
os.makedirs(STATIC_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'stock@999'

def format_market_cap(market_cap):
    if not isinstance(market_cap, (int, float)):
        return "N/A"
    if market_cap >= 1e12:
        return f"${market_cap/1e12:.2f}T"
    if market_cap >= 1e9:
        return f"${market_cap/1e9:.2f}B"
    if market_cap >= 1e6:
        return f"${market_cap/1e6:.2f}M"
    return f"${market_cap:,}"

def get_company_info(stock_obj, symbol):
    try:
        info = stock_obj.info
        name = info.get("longName", info.get("shortName", symbol))
        sector = info.get("sector", "N/A")
        market_cap = format_market_cap(info.get("marketCap", "N/A"))
    except Exception:
        name = symbol
        sector = "N/A"
        market_cap = "N/A"
    return {
        "symbol": symbol,
        "name": name,
        "sector": sector,
        "market_cap": market_cap
    }

def style_chart(ax1, ax2, valid_symbols, period):
    title_symbols = ", ".join(valid_symbols)
    if len(title_symbols) > 50:
        title_symbols = title_symbols[:47] + "..."
        
    ax1.set_title(f"Stock Analysis: {title_symbols} ({period})", fontsize=16, fontweight='bold', pad=15)
    ax1.set_ylabel("Price (USD)", fontsize=12, fontweight='bold')
    ax1.legend(loc="upper left", frameon=True, facecolor="white", shadow=True)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax2.set_xlabel("Date", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Volume", fontsize=12, fontweight='bold')
    ax2.legend(loc="upper left", frameon=True, facecolor="white", shadow=True, fontsize='small')
    ax2.grid(True, linestyle='--', alpha=0.7)

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('user'):
        flash('Please login to access the dashboard.', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'GET':
        return render_template('index.html')

    symbol_input = request.form.get('symbol', '').upper().strip()
    period = request.form.get('period', '6mo')
    
    if not symbol_input:
        flash('Please enter a stock symbol', 'error')
        return render_template('index.html', symbol=symbol_input, period=period)
        
    try:
        symbols = []
        for s in symbol_input.split(','):
            s_stripped = s.strip()
            if s_stripped:
                symbols.append(s_stripped)
        
        if len(symbols) == 0:
            flash('Please enter at least one valid stock symbol', 'error')
            return redirect(url_for('index'))

        all_data = pd.DataFrame()
        valid_symbols = []
        companies_info = []
        global_high = float('-inf')
        global_low = float('inf')
        total_close = 0
        total_days = 0
        
        plt.style.use("ggplot")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
        
        for sym in symbols:
            stock = yf.Ticker(sym)
            df = stock.history(period=period)
            
            if df.empty:
                continue
                
            valid_symbols.append(sym)
            comp_info = get_company_info(stock, sym)
            companies_info.append(comp_info)
            
            ax1.plot(df.index, df["Close"], label=f"{sym}", linewidth=2)
            ax2.fill_between(df.index, df["Volume"], alpha=0.5, label=f"{sym} Vol")
            
            if df["High"].max() > global_high:
                global_high = df["High"].max()
            if df["Low"].min() < global_low:
                global_low = df["Low"].min()
                
            total_close += df["Close"].sum()
            total_days += len(df["Close"])
            
            df_subset = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            new_columns = []
            for col in df_subset.columns:
                new_columns.append(f"{sym}_{col}")
            df_subset.columns = new_columns
            
            if all_data.empty:
                all_data = df_subset
            else:
                all_data = all_data.join(df_subset, how='outer')

        if len(valid_symbols) == 0:
            flash('No valid data found for any of the entered symbols.', 'error')
            return redirect(url_for('index'))

        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute(
                "INSERT INTO history (user_email, symbol, period) VALUES (%s, %s, %s)",
                (session['user'], symbol_input, period)
            )
            mydb.commit()
            cursor.close()
        except Exception as e:
            print("Failed to add to history:", e)

        style_chart(ax1, ax2, valid_symbols, period)
        chart_path = os.path.join(STATIC_FOLDER, "chart.png")
        plt.savefig(chart_path)
        plt.close()
        
        csv_path = os.path.join(BASE_DIR, "stock_data.csv")
        all_data.to_csv(csv_path)

        avg = round(total_close / total_days, 2)
        stats = {
            "highest": round(global_high, 2),
            "lowest": round(global_low, 2),
            "average": avg
        }
        
        chart_timestamp = int(time.time())
    except Exception as e:
        print("Failed to get stock details:", e)
        flash('Something went wrong. Please check the symbol or try again.', 'error')
        return redirect(url_for('index'))
    else:
        return render_template(
            'index.html', 
            stats=stats, 
            symbol=symbol_input, 
            period=period, 
            chart_ready=True, 
            timestamp=chart_timestamp, 
            companies=companies_info
        )

@app.route('/download')
def download():
    if not session.get('user'):
        return redirect(url_for('login'))
        
    csv_path = os.path.join(BASE_DIR, "stock_data.csv")
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)
    else:
        flash('No file available to download', 'error')
        return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        
        hashed_password = generate_password_hash(password)
        
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT count(*) FROM users WHERE email=%s', [email])
            email_count = cursor.fetchone()[0]
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verify the email')
            return redirect(url_for('signup'))
        else:
            if email_count == 0:
                try:
                    cursor = mydb.cursor(buffered=True)
                    cursor.execute('INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)', [name, email, hashed_password, role])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('Could not store user details')
                    return redirect(url_for('signup'))
                else:
                    flash('Account created successfully! Please login.', 'success')
                    return redirect(url_for('login'))
            elif email_count > 0:
                flash('Email already registered. Please login.', 'error')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT count(*) FROM users WHERE email=%s', [email])
            email_count = cursor.fetchone()[0]
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verify the email')
            return redirect(url_for('login'))
        else:
            if email_count == 1:
                try:
                    cursor = mydb.cursor(buffered=True)
                    cursor.execute('SELECT name, password, role FROM users WHERE email=%s', [email])
                    user = cursor.fetchone()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('could not get password')
                    return redirect(url_for('login'))
                else:
                    if check_password_hash(user[1], password):
                        session['user'] = email
                        session['name'] = user[0]
                        session['role'] = user[2]
                        flash('Logged in successfully!', 'success')
                        if session['role'] == 'admin':
                            return redirect(url_for('admin_dashboard'))
                        return redirect(url_for('index'))
                    else:
                        flash('invalid password')
                        return redirect(url_for('login'))
            elif email_count == 0:
                flash('No user found')
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user', None)
        session.pop('name', None)
        session.pop('role', None)
        flash('Logged out successfully.', 'success')
    else:
        flash('pls login to logout')
    return redirect(url_for('login'))

@app.route('/history')
def history():
    if not session.get('user'):
        return redirect(url_for('login'))

    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute(
            "SELECT symbol, period, created_at FROM history WHERE user_email=%s ORDER BY created_at DESC",
            [session['user']]
        )
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print("Failed to load history:", e)
        flash('Could not get the history data')
        return redirect(url_for("index"))
    else:
        return render_template('history.html', data=data)

@app.route('/add_watchlist/<symbol>')
def add_watchlist(symbol):
    if not session.get('user'):
        return redirect(url_for('login'))
        
    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute(
            "SELECT * FROM watchlist WHERE user_email=%s AND symbol=%s",
            (session['user'], symbol)
        )
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(
                "INSERT INTO watchlist (user_email, symbol) VALUES (%s,%s)",
                (session['user'], symbol)
            )
            mydb.commit()
            cursor.close()
            flash(f'{symbol} added to watchlist!', 'success')
        else:
            cursor.close()
            flash('Already in watchlist', 'error')
    except Exception as e:
        print("Failed to add to watchlist:", e)
        flash('Failed to add to watchlist.', 'error')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/watchlist')
def watchlist():
    if not session.get('user'):
        return redirect(url_for('login'))
        
    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute(
            "SELECT symbol FROM watchlist WHERE user_email=%s",
            [session['user']]
        )
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print("Failed to load watchlist:", e)
        flash('Could not get the watchlist data')
        return redirect(url_for("index"))
    else:
        return render_template('watchlist.html', data=data)

@app.route('/remove_watchlist/<symbol>')
def remove_watchlist(symbol):
    if not session.get('user'):
        return redirect(url_for('login'))
        
    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute(
            "DELETE FROM watchlist WHERE user_email=%s AND symbol=%s",
            (session['user'], symbol)
        )
        mydb.commit()
        cursor.close()
    except Exception as e:
        print("Failed to remove from watchlist:", e)
        flash('Failed to remove from watchlist.', 'error')
        return redirect(url_for('watchlist'))
    else:
        flash('Removed from watchlist', 'success')
        return redirect(url_for('watchlist'))

@app.route('/api/history')
def api_history():
    if not session.get('user'):
        return {"error": "Not authenticated"}, 401
        
    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute(
            "SELECT symbol, period FROM history WHERE user_email=%s",
            [session['user']]
        )
        data = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print("Failed to load api history:", e)
        return {"error": str(e)}, 500
    else:
        return {"data": data}

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('user') or session.get('role') != 'admin':
        flash('Unauthorized access', 'error')
        return redirect(url_for('login'))
        
    try:
        cursor = mydb.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * FROM available_stocks ORDER BY created_at DESC")
        stocks = cursor.fetchall()
        
        # update prices in realtime
        for s in stocks:
            try:
                stock_data = yf.Ticker(s['symbol'])
                current_price = stock_data.history(period="1d")['Close'].iloc[-1]
            except Exception as e:
                print("Error with price:", e)
                s['current_price'] = 'N/A'
            else:
                s['current_price'] = round(current_price, 2)
                
        cursor.close()
    except Exception as e:
        print("Failed to load admin dashboard:", e)
        stocks = []
        
    return render_template('admin_dashboard.html', stocks=stocks)

@app.route('/admin/add_stock', methods=['POST'])
def admin_add_stock():
    if not session.get('user') or session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    symbol = request.form.get('symbol', '').upper().strip()
    if not symbol:
        flash('Symbol cannot be empty', 'error')
        return redirect(url_for('admin_dashboard'))
        
    try:
        # Check validity
        stock = yf.Ticker(symbol)
        info = get_company_info(stock, symbol)
        
        if info['name'] == symbol and info['sector'] == 'N/A':
            # It might still be valid but has no info, let's verify if history works
            df = stock.history(period='1d')
            if df.empty:
                flash(f'Invalid stock symbol: {symbol}', 'error')
                return redirect(url_for('admin_dashboard'))
                
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT * FROM available_stocks WHERE symbol=%s", (symbol,))
        if cursor.fetchone():
            flash(f'{symbol} already added', 'error')
            return redirect(url_for('admin_dashboard'))
            
        cursor.execute("INSERT INTO available_stocks (symbol, name, added_by) VALUES (%s, %s, %s)", 
                       (symbol, info['name'], session['user']))
        mydb.commit()
        cursor.close()
        
    except Exception as e:
        print("Failed to add stock:", e)
        flash('Failed to add the stock.', 'error')
    else:
        flash(f'Successfully added {symbol} to available stocks.', 'success')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_stock/<symbol>')
def admin_delete_stock(symbol):
    if not session.get('user') or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute("DELETE FROM available_stocks WHERE symbol=%s", (symbol,))
        mydb.commit()
        cursor.close()
        flash(f'Successfully removed {symbol}', 'success')
    except Exception as e:
        print("Delete error:", e)
        flash('Failed to remove stock', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/available_stocks')
def available_stocks():
    if not session.get('user'):
        flash('Please login to view available stocks.', 'error')
        return redirect(url_for('login'))
        
    try:
        cursor = mydb.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * FROM available_stocks ORDER BY created_at DESC")
        stocks = cursor.fetchall()
        
        # Add realtime price
        for s in stocks:
            try:
                stock_data = yf.Ticker(s['symbol'])
                current_price = stock_data.history(period="1d")['Close'].iloc[-1]
            except Exception as e:
                print("Error with price:", e)
                s['current_price'] = 'N/A'
            else:
                s['current_price'] = round(current_price, 2)
                
        cursor.close()
    except Exception as e:
        print("Failed to load available stocks:", e)
        stocks = []
        
    return render_template('available_stocks.html', stocks=stocks)

@app.route('/buy/<symbol>', methods=['POST'])
def buy_stock(symbol):
    if not session.get('user'):
        return redirect(url_for('login'))
        
    qty = request.form.get('quantity', 1, type=int)
    
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="1d")
        if df.empty:
            flash(f'Cannot fetch price for {symbol}', 'error')
            return redirect(url_for('available_stocks'))
            
        current_price = df['Close'].iloc[-1]
        
        cursor = mydb.cursor(buffered=True)
        cursor.execute("INSERT INTO portfolio (user_email, symbol, quantity, buy_price) VALUES (%s, %s, %s, %s)",
                       (session['user'], symbol, qty, float(current_price)))
        mydb.commit()
        cursor.close()
        
    except Exception as e:
        print("Failed to buy stock:", e)
        flash('Failed to complete transaction.', 'error')
    else:
        flash(f'Successfully bought {qty} shares of {symbol} at ${current_price:.2f}', 'success')
        
    return redirect(url_for('portfolio'))

@app.route('/portfolio')
def portfolio():
    if not session.get('user'):
        return redirect(url_for('login'))
        
    try:
        cursor = mydb.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * FROM portfolio WHERE user_email=%s ORDER BY buy_date DESC", (session['user'],))
        holdings = cursor.fetchall()
        
        total_investment = 0
        current_value = 0
        
        for h in holdings:
            inv = float(h['buy_price']) * int(h['quantity'])
            total_investment += inv
            h['investment'] = inv
            
            try:
                stock_data = yf.Ticker(h['symbol'])
                cp = stock_data.history(period="1d")['Close'].iloc[-1]
            except Exception as e:
                print("Error loading price:", e)
                h['current_price'] = 'N/A'
                h['current_value'] = 'N/A'
                h['profit_loss'] = 'N/A'
            else:
                h['current_price'] = round(cp, 2)
                cv = cp * int(h['quantity'])
                current_value += cv
                h['current_value'] = round(cv, 2)
                h['profit_loss'] = round(cv - inv, 2)
                
        cursor.close()
    except Exception as e:
        print("Failed to load portfolio:", e)
        holdings = []
        total_investment = 0
        current_value = 0
        
    return render_template('portfolio.html', holdings=holdings, total_investment=round(total_investment, 2), current_value=round(current_value, 2))

if __name__ == '__main__':
    app.run(debug=True)