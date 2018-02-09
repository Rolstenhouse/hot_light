# server.py
from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, url_for
import requests

app = Flask(__name__, static_folder="./static", template_folder="./templates")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/json")
def json():
  resp = requests.get("https://services.krispykreme.com/api/locationsearchresult/?callback=load&responseType=Full&search=%7B%22Where%22%3A%7B%22LocationTypes%22%3A%5B%22Store%22%2C%22Commissary%22%2C%22Franchise%22%5D%2C%22OpeningDate%22%3A%7B%22ComparisonType%22%3A0%7D%7D%2C%22Take%22%3A%7B%22Min%22%3A3%2C%22DistanceRadius%22%3A100%7D%2C%22PropertyFilters%22%3A%7B%22Attributes%22%3A%5B%22FoursquareVenueId%22%2C%22OpeningType%22%5D%7D%7D&lat=29.6516344&lng=-82.32482619999996&_=1517112369718")

  print(resp.text, file=sys.stderr)

  return (resp.text, resp.status_code, resp.headers.items())

if __name__ == "__main__":
  app.run(debug=True) 