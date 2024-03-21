#!/usr/bin/env python3
'''
   Module for application routes
'''
from mainapp import app, db
from flask import render_template, url_for, redirect, flash
from mainapp.forms import Permit
from datetime import datetime
from mainapp.models import Street, Space
import sqlalchemy as sa


@app.route('/')
@app.route('/home')
def home():
    '''
       view function for the home page
    '''
    return render_template('home.html', title='Home')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    '''
       view function to render the application form
    '''
    form = Permit()
    if form.validate_on_submit():
        data = form.data
        start_date = data['start_date']
        end_date = data['end_date']

        if start_date >= end_date:
            flash('Start date must be before end date.','error')
            return render_template('application_form.html', title='application', form=form)

        if start_date < datetime.now().date():
            flash('Start date cannot be in the past.', 'error')
            return render_template('application_form.html', title='application', form=form)

        vendor_name = data['vendor_name']
        vendor_email = data['vendor_email']
        street_name = data['street_name']
        space_number = data['space_number']
        about_business = data['about_business']
        street_space = (
                db.session.query(Street)
                .join(Space, Street.street_id == Space.street_id)
                .filter(Space.space_number == space_number)  
                .filter(Street.street_name == street_name)
                .first()
                )
        if street_space is None:
            flash(f'{street_name} does not have {space_number}')
            return render_template('application_form.html', title='application', form=form)
        return redirect(url_for('home'))

    return render_template('application_form.html', title='application', form=form)

