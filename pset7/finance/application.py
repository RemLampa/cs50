from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    return apology("TODO")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # get user's remaining funds
    rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session.get("user_id"))
    wallet = rows[0]["cash"]
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        
        # ensure stock symbol was submitted
        if not symbol:
            flash("Please enter a stock symbol.", "danger")
            return render_template("buy.html", wallet=wallet)
        
        stock_quote = lookup(symbol.upper())
        
        # ensure stock symbol is valid
        if stock_quote is None:
            flash("Please enter a valid stock symbol.", "danger")
            return render_template("buy.html", wallet=wallet)
            
        # ensure number of shares is a positive integer
        try:
            shares = int(request.form.get("shares"))
            
            if shares <= 0:
                raise Exception()
        except:
            flash("Please enter valid number of shares.", "danger")
            return render_template("buy.html", wallet=wallet)
        
        # get total purchase cost
        total_cost = shares * stock_quote["price"]
        
        # ensure funds are sufficient
        if total_cost > wallet:
            flash("You have insufficient funds.", "danger")
            return render_template("buy.html", wallet=wallet)
        
        # find stock under user's account
        rows = db.execute("SELECT * FROM stocks WHERE symbol = :symbol AND owner_id = :owner_id",
            symbol=stock_quote["symbol"],
            owner_id=session.get("user_id"))
        
        # if user already has shares of purchased stock, update
        if len(rows) == 1:
            total_shares = rows[0]["shares"] + shares
            db.execute("UPDATE stocks SET shares = :total_shares WHERE id = :id",
                total_shares=total_shares,
                id=rows[0]["id"])
        # else, add stock in user's account
        else:
            db.execute("INSERT INTO stocks(symbol, owner_id, shares) VALUES(:symbol, :owner_id, :shares)",
                symbol=stock_quote["symbol"],
                owner_id=session.get("user_id"),
                shares=shares)
        
        # subtract purchase cost from wallet
        wallet = wallet - total_cost
        
        # update user wallet in database
        rows = db.execute("UPDATE users SET cash = :wallet WHERE id = :id", wallet=wallet, id=session.get("user_id"))
        
        return render_template("buy.html", quote=stock_quote, shares=shares, cost=total_cost, wallet=wallet)
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html", wallet=wallet)

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        
        if not symbol:
            return apology("enter a stock symbol")
        
        stock_quote = lookup(symbol.upper())
        
        if stock_quote is None:
            return apology("invalid stock symbol")
        
        return render_template("quote.html", quote=stock_quote)
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user is already logged in
    if session.get("user_id"):
        return redirect(url_for("index"))
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        
        # ensure username was submitted
        if not username:
            return apology("must provide username")

        # ensure password was submitted
        elif not password:
            return apology("must provide password")
            
        # ensure password confirmation was submitted
        elif not confirm_password:
            return apology("must confirm password")
            
        # ensure passwords must match
        elif password != confirm_password:
            return apology("passwords must match")
            
        # encrypt password
        hashed_password = pwd_context.hash(password)
        
        # create new user
        success = db.execute("INSERT INTO users(username, hash) VALUES(:username, :password)",
            username=username,
            password=hashed_password)
        
        # redirect to login if successfully registered
        if success:
            flash('You were successfully registered! You may now log in.')
            return redirect(url_for("login"))
        else:
            return apology("registration error")
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")    

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    return apology("TODO")
