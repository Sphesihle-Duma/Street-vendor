#!/usr/bin/env python3
'''
   A module for models representing tables
'''
from datetime import datetime, timezone
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
    spaces: so.WriteOnlyMapped['Space'] = so.relationship(back_populates='street')

    def __repr__(self):
        '''
           String represantation of the street object
        '''
        return '<User {}>'.format(self.street_name)


class Space(db.Model):
    '''
        A model representing a space table
    '''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    space_number: so.Mapped[int] = so.mapped_column(unique=True, index=True)
    street_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Street.street_id),
                                                 index=True)
    street: so.Mapped[Street] = so.relationship(back_populates='spaces')

    def __repr__(self):
        '''
           string represention of the space object
        '''
        return '<Space {}>'.format(self.space_number)


class Permit(db.Model):
    '''
       A model representing permit table
    '''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    vendor_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    vendor_email: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                    unique=True)
    street_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    space_number: so.Mapped[int] = so.mapped_column(index=True, unique=True)
    about_business: so.Mapped[str] = so.mapped_column(sa.String(140))
    start_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime)
    end_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime)
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    status: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    def __repr__(self):
        '''
           Sting representation of permit object
        '''
        return '<Permit {}>'.format(self.vendor_name)
