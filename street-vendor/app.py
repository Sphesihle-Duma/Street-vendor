#!/usr/bin/env python3
'''
   The main application
'''
from mainapp import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from mainapp.models import Street, Space, Permit, User

@app.shell_context_processor
def make_shell_context():
    '''
       Setting flask shell context
    '''
    context_dict = {
            'sa': sa,
            'so': so,
            'db': db,
            'Street': Street,
            'Space': Space,
            'Permit': Permit,
            'User': User
            }
    return context_dict


if __name__ == '__main__':
    app.run(debug=True)
