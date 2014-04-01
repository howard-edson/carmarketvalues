#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: run_searches.py
"""
This module is intended to be scheduled in a cron job to run nightly, but
needs access to the django environment and models, so it can
read Searches from the database, fetch new postings for each search,
and insert them into the database. 

"""
# make it possible to leverage our django models in this script
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmv_project.settings")
from cmv_app.models import Search, Posting
import feedparser
import re
import datetime
import HTMLParser

pars = HTMLParser.HTMLParser()


# Establish upper and lower limits for a "reasonable" year
MIN_REASONABLE_VEHICLE_YEAR = 1940
MAX_REASONABLE_VEHICLE_YEAR = datetime.date.today().year + 1


# the pattern used to identify the vehicle year from the posting title
p_year = re.compile(  # matches any year between 1900-2999
    u"""
    (?<!\$|\d)      # year can't be preceded by $ or digit
    (19[456789]\d   # 1940-1999
     |              # ...or...
     20\d{2})       # 2000-2099
    (?!\d)          # year can't be followed immediatley by a digit
    """,
    re.UNICODE | re.VERBOSE)

# the pattern used to identify the vehicle price from the posting title
p_price = re.compile(  # matches an integer with 3-6 digits preceded by a $
    u"""
    (?<=\$)     # price must be preceded by a $
    \d{3,6}     # 3 to 6 digits (there is reliably no comma separator in craigslist prices)
    $           # price reliably appears at the end of a posting title
    """,
    re.UNICODE | re.VERBOSE)


def make_url(search, region):
    "Return a URL to be queried for a search, region."
    
    url = "http://{region}.craigslist.org/search/".format(region=region)
    url += "ct{seller_type}?catAbb=ct{seller_type}".format(seller_type = search.seller_type)
    query = ""
    if search.vehicle_make:
        query += '+{make}'.format(make=search.vehicle_make)
    if search.vehicle_model:
        query += '+{model}'.format(model=search.vehicle_model)
    if search.extra_keywords:
        query += '+{keywords}'.format(keywords=search.extra_keywords)
    if query:
        url += "&query={}".format(query)
    if search.min_price:
        url += "&minAsk={min_price}".format(min_price = search.min_price)
    if search.max_price:
        url += "&maxAsk={max_price}".format(max_price = search.max_price)
    if search.min_year:
        url += "&autoMinYear={min_year}".format(min_year = search.min_year)
    if search.max_year:
        url += "&autoMaxYear={max_year}".format(max_year = search.max_year)
    if search.pic_only:
        url += "&hasPic=1"
    if search.search_title_only:
        url += "&srchType=T"
    url += "&format=rss"
    return url


class Entry(object):
    """
    Represents a single entry (posting) retrieved from craigslist rss feed.
    Prepares the elements needed to create a Posting object.

    """
    def __init__(self, entry):
        # It appears to be necessary to "unescape" the text in the feed
        # to keep funny html characters out of our data. 
        pars = HTMLParser.HTMLParser()
        self.posting_url = pars.unescape(entry[u'id'])
        self.vehicle_year = None
        self.vehicle_price = None
        self.title = pars.unescape(entry[u'title'])
        self.body = pars.unescape(entry[u'summary'])

        # parse year from title (if possible)
        potential_years = p_year.findall(self.title)
        if potential_years:
            # there may be more than one potential year found in title
            for year in potential_years:
                year = int(year)
                if (MIN_REASONABLE_VEHICLE_YEAR <= year <= MAX_REASONABLE_VEHICLE_YEAR):
                    self.vehicle_year = year
                    break  # exit loop early with first reasonable year found

        # parse price from title (if possible)
        match_object = p_price.search(self.title)
        if match_object:
            self.vehicle_price = int(match_object.group(0))


if __name__ == "__main__":

    # process all searches from the database
    searches = Search.objects.all()
    for search in searches:
        for region in search.regions.all():
            search_url = make_url(search, region)
            postings = []  # a list of postings retrieved for this search_url
            doc = feedparser.parse(search_url)
            for entry in doc.entries:
                e = Entry(entry)
                if not ('wanted' in e.title or 'wtb' in e.title):
                    # update or insert a new posting in the database
                    try:
                        posting = Posting.objects.get(posting_url=e.posting_url)
                    except Posting.DoesNotExist:
                        posting = Posting(region=region,
                                      posting_url=e.posting_url,
                                      vehicle_year=e.vehicle_year,
                                      vehicle_price=e.vehicle_price,
                                      title=e.title,
                                      body=e.body)
                        posting.save()
                    finally:
                        posting.search.add(search)
