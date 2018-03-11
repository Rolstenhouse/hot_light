from flask import Flask
from flask_pymongo import PyMongo, MongoClient
from flask_mail import Mail
import secrets
import os

def create_app():
  app = Flask(__name__, static_folder="./static", template_folder="./templates")

  app.config['MONGO_URI'] = 'mongodb://'+os.environ['MONGO_USER']+':'+os.environ['MONGO_PASSWORD']+'@ds149905.mlab.com:49905/krispykreme'
  app.config['MONGO_CONNECT'] = False # Necessary for multi processing execution

  app.config['MAIL_SERVER']='smtp.gmail.com'
  app.config['MAIL_PORT']=465
  app.config['MAIL_USERNAME']=os.environ['EMAIL_USER']
  app.config['MAIL_PASSWORD']=os.environ['EMAIL_PASSWORD']
  app.config['MAIL_USE_TLS'] = False
  app.config['MAIL_USE_SSL'] = True

  return app