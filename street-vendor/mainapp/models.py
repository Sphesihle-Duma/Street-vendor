#!/usr/bin/env python3
'''
   A module for models representing tables
'''
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from mainapp import db

class Street(db.Model):
    '''
       A model representing street table
    '''
    street_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    street_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                   unique=True)

    def __repr__(self):
        '''
           String represantation of the street object
        '''
        return '<User {}>'.format(self.street_name)
