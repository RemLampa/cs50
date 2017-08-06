import csv
import urllib.request

from flask import redirect, render_template, request, session, url_for
from functools import wraps

def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.endpoint))
        return f(*args, **kwargs)
    return decorated_function

def lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # reject symbol if it contains comma
    if "," in symbol:
        return None

    # query Yahoo for quote
    # http://stackoverflow.com/a/21351911
    try:
        url = "http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s={}".format(symbol)
        webpage = urllib.request.urlopen(url)
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())
        row = next(datareader)
    except:
        return None

    # ensure stock exists
    try:
        price = float(row[2])
    except:
        return None

    # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
    return {
        "name": row[1],
        "price": price,
        "symbol": row[0].upper()
    }

def usd(value):
    """Formats value as USD."""
    
    return "${:,.2f}".format(value)

def get_stock_info(stock):
    lookup_info = lookup(stock["symbol"])
    
    value = stock["shares"] * lookup_info["price"]
    
    stock_info = {
        "id": stock["id"],
        "symbol": stock["symbol"],
        "name": lookup_info["name"],
        "shares": stock["shares"],
        "price": lookup_info["price"],
        "value": value
    }
    
    return stock_info

def get_stocks(db, user_id):
    """Retrieves list of user's stocks"""
    
    rows = db.execute("SELECT id, symbol, shares FROM stocks WHERE owner_id = :owner_id ORDER BY symbol ASC",
        owner_id=user_id)
    
    if len(rows) > 0:
        stocks = []
        for row in rows:
            # don't show stocks with 0 shares
            if row["shares"] == 0:
                continue
            
            stock = get_stock_info(row)
            
            stocks.append(stock)
    else:
        stocks = None
        
    return stocks