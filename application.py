import datetime
import requests
import math

from collections import OrderedDict
from flask import Flask
from flask import render_template

app = Flask(__name__)

API = {
    'information': "https://valencefr.publicbikesystem.net/ube/gbfs/v1/en/station_information",
    'status': "https://valencefr.publicbikesystem.net/ube/gbfs/v1/en/station_status"
}

station_information = None

@app.route("/")
def index():
    global station_information

    if station_information is None:
        req = requests.get(API['information'])
        station_information = req.json()['data']['stations']

    req = requests.get(API['status'])
    station_status = req.json()['data']['stations']

    info_dict = {s['station_id']: s for s in station_information}
    status_dict = {s['station_id']: s for s in station_status}

    for k, v in info_dict.items():
        v.update(status_dict[k])

    custom_order = (
        "49",  # Saint-Péray République
        "3",  # Gare
        "2",  # Pôle bus
        "6",  # Basse ville
        "46",  # Maladière
    )

    def compare(pair):
        try:
            return custom_order.index(pair[0])
        except ValueError:
            return math.inf

    info_dict = OrderedDict(sorted(info_dict.items(), key=compare))

    context = {
        'stations': info_dict,
        'now': datetime.datetime.now().strftime('%H:%M')
    }
    return render_template('index.html', **context)
