#!/usr/bin/env python3
'''
   Module for creating forms
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms import PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
import sqlalchemy as sa
from mainapp import db
from mainapp.models import Space, Street


class PermitForm(FlaskForm):
    '''
       A form for applying for a permit
    '''
    vendor_name = StringField('Vendor name', validators=[DataRequired()])
    vendor_email = StringField('Vendor email', validators=[DataRequired(), Email()])
    street_name = SelectField('Street name', coerce=str, validators=[DataRequired()])
    space_number = SelectField('Street number', coerce=int, validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End date', validators=[DataRequired()], format='%Y-%m-%d')
    about_business = TextAreaField('Nature of business', validators=[Length(min=0, max=140), DataRequired()]) 
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        '''
           A constructor for initializing
        '''
        super(PermitForm, self).__init__(*args, **kwargs)

        self.space_number.choices = [space.space_number for space in Space.query.all()]
        self.street_name.choices = [street.street_name for street in Street.query.all()]


class LoginForm(FlaskForm):
    '''
       login form to capture login details
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')
