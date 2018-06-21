#coding:utf-8
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = "any random string"
db = SQLAlchemy(app)
import aguia.models
db.create_all()
import aguia.controllers
