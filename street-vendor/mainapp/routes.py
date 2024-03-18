#!/usr/bin/env python3
'''
   Module for application routes
'''
from mainapp import app
from flask import render_template
from mainapp.forms import Permit


@app.route('/')
@app.route('/home')
def home():
    '''
       view function for the home page
    '''
    return render_template('home.html', title='Home')

@app.route('/apply')
def apply():
    '''
       view function to render the application form
    '''
    form = Permit()
    return render_template('application_form.html', title='application', form=form)

