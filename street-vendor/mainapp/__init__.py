#!/usr/bin/env python3
'''
   creating members of the package
'''
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from mainapp import routes
