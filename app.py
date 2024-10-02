from flask import Flask, jsonify, request,render_template
import logging
logging.basicConfig(filename='error.log',level=logging.ERROR,format='%(asctime)s:%(levelname)s:%(message)s')
import sys
import requests
import folium
from geopy.geocoders import Nominatim

import flask
app = Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('findLocation.html')



@app.route('/findLocation', methods=['POST'])

def predict():

    mcc = request.form.get("mcc")
    mnc = request.form.get("mnc")
    lac = request.form.get("lac")
    cid = request.form.get("cid")
    params = {"mcc": mcc, #mobileCountryCode
          "mnc": mnc, #mobileNetworkCode
          "lac": lac, #locationAreaCode
          "cell_id": cid #CellId
         }
    #Set the url to the appropriate API endpoint location
    url = "https://opencellid.org/ajax/searchCell.php"

    r = requests.get(url, params=params)
    if not r.ok or r.text == '"Invalid Request"' or r.text == 'false': 
    # display the response if something went wrong...
        print('Error: '+r.text)
        return flask.render_template('error.html')
    
    # Display the response
    print(r.json())

    lon = r.json()["lon"]
    lat = r.json()["lat"]

    # initialize Nominatim API
    geolocator = Nominatim(user_agent="Mobile_Location_Finder")
 
 
    # Latitude & Longitude input
    Latitude = lat
    Longitude = lon
 
    location = geolocator.reverse(Latitude+","+Longitude)
 
    address = location.raw['address']
    print(address)

    m = folium.Map([lat, lon], zoom_start=15)

    folium.Marker(
        location=[lat, lon],
        tooltip="Your Location",
        popup=address,
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)

    m.save('templates/mapLocation.html')
    return flask.render_template('mapLocation.html')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
