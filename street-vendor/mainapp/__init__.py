#!/usr/bin/env python3
'''
   creating members of the package
'''
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from mainapp import routes
