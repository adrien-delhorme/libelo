import datetime
import math
import pybikes

from collections import OrderedDict
from flask import Flask
from flask import render_template
from flask import request, redirect

app = Flask(__name__)

station_information = None

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        context = {
            "bike_services": sorted(pybikes.get_instances(), key=lambda service: service[0])
        }
        return render_template("index.html", **context)
    elif request.method == "POST":
        return redirect(f"/{request.form['bike_service']}/")


@app.route("/<string:bike_service_name>/")
def stations(bike_service_name):
    favorites = request.args.getlist("fav")
    
    bike_service = pybikes.get(bike_service_name)
    
    try:
        bike_service.update()
    except:
        bike_service = None

    if bike_service is not None:
        def compare(pair):
            try:
                return favorites.index(pair.extra["uid"])
            except ValueError:
                return math.inf

        # Display user favorites stations first, and keep the order
        stations = sorted(bike_service.stations, key=compare)

        context = {
            "bike_service": bike_service,
            "stations": stations,
            "favorites": favorites,
            "now": datetime.datetime.now().strftime("%H:%M")
        }
        return render_template("stations.html", **context)
        
    else:
        return render_template("error.html")

