#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: insert_regions.py
"""
Demonstrates use of a python script to populate the Regions table, using
our Region model and the django queryset api. 

"""
# make it possible to leverage our django models in this script
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmv_project.settings")
from cmv_app.models import Region

# a list of major US metro areas on craigslist
regions = [
    'atlanta',
    'austin',
    'boston',
    'chicago',
    'dallas',
    'denver',
    'detroit',
    'houston',
    'lasvegas',
    'losangeles',
    'miami',
    'minneapolis',
    'newyork',
    'orangecounty',
    'philadelphia',
    'phoenix',
    'portland',
    'raleigh',
    'sacramento',
    'sandiego',
    'seattle',
    'sfbay',
    'washingtondc'
]

Region.objects.all().delete()

for region in regions:
    Region.objects.create(name=region)
