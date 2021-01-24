import datetime
import requests

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

    info_dict = OrderedDict(sorted(info_dict.items(), key=lambda x: x[1]['name']))

    context = {
        'stations': info_dict,
        'now': datetime.datetime.now().strftime('%H:%M')
    }
    return render_template('index.html', **context)
