#!/usr/bin/env python3
'''
   Module for creating forms
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class Permit(FlaskForm):
    '''
       A form for applying for a permit
    '''
    vendor_name = StringField('Vendor name', validators=[DataRequired()])
    vendor_email = StringField('Vendor email', validators=[DataRequired(), Email()])
    street_name = StringField('Street name', validators=[DataRequired()])
    space_number = SelectField('Street number', choices=[1, 2, 3, 4], validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End date', validators=[DataRequired()], format='%Y-%m-%d')
    about_business = TextAreaField('Nature of business', validators=[Length(min=0, max=140)]) 
    submit = SubmitField('Submit')
