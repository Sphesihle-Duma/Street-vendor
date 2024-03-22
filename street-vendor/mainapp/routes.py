#!/usr/bin/env python3
'''
   Module for application routes
'''
from mainapp import app, db
from flask import render_template, url_for, redirect, flash
from mainapp.forms import PermitForm, LoginForm
from datetime import datetime
from mainapp.models import Street, Space, Permit
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc


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
    form = PermitForm()
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
        registered_vendor = (
                db.session.query(Permit)
                .filter(Permit.vendor_email == vendor_email)
                .first()
                )
        if registered_vendor:
            flash('You already have a permit')
            return render_template('application_form.html', title='application', form=form)
        taken_space = (
                db.session.query(Permit)
                .filter(Permit.street_name == street_name)
                .filter(Permit.space_number == space_number)
                .first()
                )
        if taken_space:
            flash(f'The {space_number} on {street_name} is taken')
            return render_template('application_form.html', title='application', form=form)

        new_permit = Permit(
                    vendor_name=vendor_name,
                    vendor_email=vendor_email,
                    street_name=street_name,
                    space_number=space_number,
                    about_business=about_business,
                    start_date=start_date,
                    end_date=end_date,
                    status='Pending'
                    )
        try:
            db.session.add(new_permit)
            db.session.commit()
            flash('Permit record added successfully!', 'success')
        except sa_exc.SQLAlchemyError as e:
            db.session.rollback()
            flash('Failed to add permit record. Please try again.', 'error')
            print(f"Error: {str(e)}")
            return redirect(url_for('apply'))

        return redirect(url_for('home'))

    return render_template('application_form.html', title='application', form=form)


@app.route('/login')
def login():
    '''
       View function that renders login form
    '''
    form = LoginForm()
    return render_template('login.html', title='login', form=form)
