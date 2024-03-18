#!/usr/bin/env python3
'''
   Configuration module
'''

import os


class Config:
    '''
       Configuration class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
