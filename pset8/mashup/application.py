import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from cs50 import SQL
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/articles")
def articles():
    """Look up articles for geo."""
    
    geo = request.args.get("geo")
    
    articles = []

    if not geo:
        raise RuntimeError("geo required")

    if not re.search("^\d*$", geo):
        raise RuntimeError("invalid geo")
        
    try:
        articles = lookup(geo)
    except:
        raise RuntimeError("an error occurred")

    return jsonify(articles)

@app.route("/search")
def search():
    """Search for places that match query."""

    q = request.args.get("q")
    
    if not q:
        raise RuntimeError("q string required")
    
    try:
        results = []
        
        # postal code
        if re.search("^\d*$", q):
            results = db.execute("SELECT * FROM places WHERE postal_code LIKE :q LIMIT 10", q=q + "%")
        # name of place
        else:
            q_array = re.split(",+|,", q)
            
            q_array = list(map((lambda q_item: q_item.strip() + "%"), q_array))
            
            q_array_length = len(q_array)

            if q_array_length > 3:
                raise RuntimeError("invalid query length")
                
            if q_array_length is 3:
                results = db.execute("""
                    SELECT
                        *
                    FROM
                        places
                    WHERE
                        place_name LIKE :city
                    AND
                        (
                            admin_name1 LIKE :state
                        OR
                            admin_code1 LIKE :state
                        )
                    AND
                        country_code LIKE :country_code
                    LIMIT 10
                """,
                city=q_array[0],
                state=q_array[1],
                country_code=q_array[2])
                
            if q_array_length is 2:
                results = db.execute("""
                    SELECT
                        *
                    FROM
                        places
                    WHERE
                        place_name LIKE :city
                    AND
                        (
                            admin_name1 LIKE :state
                        OR
                            admin_code1 LIKE :state
                        OR
                            country_code LIKE :country_code
                        )
                    LIMIT 10
                """,
                city=q_array[0],
                state=q_array[1],
                country_code=q_array[1])
                
            if q_array_length is 1:
                results = db.execute("""
                    SELECT
                        *
                    FROM
                        places
                    WHERE
                        place_name LIKE :city
                    OR
                        admin_name1 LIKE :state
                    OR
                        admin_code1 LIKE :state
                    OR
                        country_code LIKE :country_code
                    LIMIT 10
                """,
                city=q_array[0],
                state=q_array[0],
                country_code=q_array[0])
    except:
        raise RuntimeError("failed to fetch from database")

    return jsonify(results)

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
