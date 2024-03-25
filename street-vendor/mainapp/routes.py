#!/usr/bin/env python3
'''
   Module for application routes
'''
from mainapp import app, db, mail
from flask import render_template, url_for, redirect, flash, request, abort
from mainapp.forms import PermitForm, LoginForm
from datetime import datetime
from mainapp.models import Street, Space, Permit, User
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from flask_mail import Message
from urllib.parse import urlsplit
import sqlalchemy.exc as sa_exc
import logging


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


@app.route('/login', methods=['POST', 'GET'])
def login():
    '''
       View function that renders login form
    '''
    if current_user.is_authenticated:
        query = sa.select(Permit)
        permits = db.session.scalars(query).all()
        return render_template('dashboard.html', title='dashboard', permits=permits)

    form = LoginForm()

    if form.validate_on_submit():
        form_data = form.data
        query = sa.select(User).where(User.username == form_data['username'])
        user = db.session.scalar(query)

        if user is None:
            flash('Invalid username')
            return redirect(url_for('login'))

        if not user.check_password(form_data['password']):
            flash('Incorrect password')
            return redirect(url_for('login'))

        login_user(user, remember=form_data['remember_me'])
        query = sa.select(Permit)
        permits = db.session.scalars(query).all()
        return render_template('dashboard.html', title='dashboard', permits=permits)

    return render_template('login.html', title='login',form=form)

@app.route('/logout')
def logout():
    '''
       Logging user out
    '''
    logout_user()
    return redirect(url_for('home'))

@app.route('/update_permit', methods=['PUT'])
def send_mail():
    '''
       Updating the permit status and  send the email
    '''
    data = request.get_json()
    new_status = data.get('new_status')
    recipient_email = data.get('email')
    app.logger.info('Recieved data: {data}')

    # Check if new_status and email are provided
    if not data or 'new_status' not in data or 'email' not in data:
        flash('Invalid request payload')
        abort(400)

    # Query the database to find the permit by vendor email
    query = sa.select(Permit).where(Permit.vendor_email == recipient_email)
    permit = db.session.scalar(query)
    print(permit.vendor_email)

    # Check if the permit
    if not permit:
        flash('Permit not found')
        abort(404)

    space_num = permit.space_number
    query = sa.select(Space).where(Space.space_number == space_num)
    space = db.session.scalar(query)
    if new_status == 'Approved':
        space.availability = 'Occupied'

    # Update the permit status to the new status
    permit.status = new_status

    try:
        db.session.commit()
        print('after commiting')
        flash('Successfully updated the status')
        print('The status was successfully updated')
        return redirect(url_for('login'))

    except Exception as e:
        db.session.rollback()
        flash(f'The status was updated {str(e)}')
        return redirect(url_for('login'))

@app.route('/spaces')
def find_space():
    '''
       view function for searching available spaces
    '''
    spaces = db.session.query(Space, Street).join(
                                                    Street, 
                                                    Street.street_id == Space.street_id
                                                    ).all()
    for space, street in spaces:
        print(f"Space: {space.space_number} {space.availability}, Street: {street.street_name}")
    return render_template('spaces.html', title='spaces', spaces=spaces)
