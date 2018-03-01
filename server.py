# server.py
from __future__ import print_function # In python 2.7
from flask import render_template, request, jsonify
from pymongo import MongoClient
import secrets
import threading
import requests
import re
import init
from emails import emails
from flask_mail import Mail, Message

# URI
client = MongoClient('mongodb://'+secrets.user+':'+secrets.password+'@ds149905.mlab.com:49905/krispykreme')
db = client.krispykreme

# Set python mongo connection on environment variable
app = init.create_app()
mail = Mail(app)

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

@app.route("/api/phone", methods=['POST'])
def phone_number():
  phone = str(request.form['phone'])
  print(phone)

  # Regex ^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\s*$
  match = re.search('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', phone)
  if not match:
    return jsonify({'failure':0})

  # Get only decimals
  number = re.sub(r"\D", "", phone)

  # Insert data into mongoDB
  numbers = db.phone_number
  numbers.insert_one({'phone': phone}).inserted_id 

  return jsonify({'success':1})


def send_messages():
  print('threaded task called')
  with app.app_context():
    print('gotten context')
    numbersdb = db.phone_number
    numbers = numbersdb.find({})
    # Send Email
    with mail.connect() as conn:  
      for number in numbers:
        phone = number['phone']
        for email in emails:
          msg = Message(recipients=[phone+email],
                        body='Krispy Kreme hotlight is on!',
                        subject='',
                        sender='isthekrispykremehotlighton@gmail.com')
          conn.send(msg)
          print('attempted to send to ')
      
    # Delete all documents from DB
    numbersdb.delete_many({})
  
mail_thread = threading.Thread(target=send_messages, args=(), kwargs={})

@app.route("/api/update_hotlight", methods=['POST'])
def update_hotlight():
  # timestamp: date
  # hot :boolean
  
  timestamp = request.form['timestamp']
  hot = request.form['hot']

  # Check hot variable
  if hot != 'True' and hot != 'False':
    return jsonify({'failure':0})

  if hot == 'True':
    # async call here
    if not mail_thread.is_alive():
      mail_thread.start()
    

  hotlight_status = db.hotlight_status
  hotlight_status.insert_one({'timestamp': timestamp, 'hot': hot}).inserted_id

  return jsonify({'success':1})

if __name__ == "__main__":
  app.run(debug=True) 