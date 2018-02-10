# server.py
from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, url_for, request
import requests
import threading
import datetime

app = Flask(__name__, static_folder="./static", template_folder="./templates")

hot_locations = {}
#unique_id: count

def poll(poll_stop):
    # Poll the server
    # Figure out later
    requests.get('http://dev-isthekrispykremehotlighton.herokuapp.com')
    if not poll_stop.is_set():
        # call again in five pinutes
        threading.Timer(60*5, poll, [poll_stop]).start()

poll_stop = threading.Event()
poll(poll_stop)
# stop the thread when needed
#poll_stop.set()

@app.route("/")
def index():
  return render_template("index.html")

# Takes latitude and longitude as arguments
@app.route("/api", methods=['GET'])
def api():

  latitude = request.args.get('latitude')
  longitude = request.args.get('longitude')

  # Stuck on browser location
  latitude = '29.6516344'
  longitude = '-82.32482619999996'

  resp = requests.get("https://services.krispykreme.com/api/locationsearchresult/?callback=load&responseType=Full&search=%7B%22Where%22%3A%7B%22LocationTypes%22%3A%5B%22Store%22%2C%22Commissary%22%2C%22Franchise%22%5D%2C%22OpeningDate%22%3A%7B%22ComparisonType%22%3A0%7D%7D%2C%22Take%22%3A%7B%22Min%22%3A3%2C%22DistanceRadius%22%3A100%7D%2C%22PropertyFilters%22%3A%7B%22Attributes%22%3A%5B%22FoursquareVenueId%22%2C%22OpeningType%22%5D%7D%7D&lat="+latitude+"&lng="+longitude+"&_=1517112369718")

  # If it's hot, save datetime to database

  return (resp.text, resp.status_code, resp.headers.items())

@app.route("/api/last-open")
def count():
  # Unique ID associated with the shop
  location_id = request.args.get('id')
  
  # Returns datetime in whatever it came in as 
  if location_id != None:
    date = hot_locations[location_id]

  # Do some sort of localization

  return date

def insertTime(id, datetime):
  pass 

if __name__ == "__main__":
  app.run(debug=True) 