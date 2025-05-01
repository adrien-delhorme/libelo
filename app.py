import httpx
import datetime
import math

from collections import OrderedDict
from flask import Flask
from flask import render_template
from flask import request, redirect

app = Flask(__name__)

station_information = None
API_BASE_URL = "http://api.citybik.es/v2"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        context = httpx.get(f"{API_BASE_URL}/networks/").json()
        return render_template("index.html", **context)
    elif request.method == "POST":
        return redirect(f"/{request.form['network']}/")


@app.route("/<string:network_id>/")
def stations(network_id):
    favorites = request.args.getlist("fav")
    
    context = httpx.get(f"{API_BASE_URL}/networks/{network_id}?fields=id,name,location,stations", follow_redirects=True).json()

    def compare(other):
        try:
            return (favorites.index(other["id"]), other["id"])
        except ValueError:
            return (math.inf, other["id"])

    # Display user favorites stations first, and keep the order
    context["network"]["stations"] = sorted(context["network"]["stations"], key=compare)

    context.update({
        "favorites": favorites,
        "now": datetime.datetime.now().strftime("%H:%M")
    })
    return render_template("stations.html", **context)
        

