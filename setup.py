"""Sets up the package"""

#!/usr/bin/env python
 # -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE.md') as f:
    LICENSE = f.read()

setup(
    name='fare_is_fair',
    version='0.1.0',
    description='Interactive SMS-Browser Game',
    long_description=README,
    author='Emily Stebbins',
    author_email='stebbins.e@gmail.com',
    url='https://github.com/estebbins/FareIsFair-API',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
