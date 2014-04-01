#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: analyze_searches.py
"""
For now this is just scratch for my prototype code related to analyzing
postings.

"""

def average_price(postings):
    """returns the average vehicle price for a list of Posting objects"""
    # get a list of prices, filtering out any None's
    prices = [i.vehicle_price for i in postings if i.vehicle_price]
    if prices:
        return  int(sum(prices) / len(prices))
    else:
        return None


def average_year(postings):
    """returns the average vehicle year for a list of Posting objects"""
    # get a list of years, filtering out any None's
    years = [i.vehicle_year for i in postings if i.vehicle_year]
    if years:
        return  int(sum(years) / len(years))
    else:
        return None


#         # Print summary analysis for marketplace
#         print url
#         print '\n%s postings processed' % len(region_postings)
#         print 'average price: $%s' % "{:,}".format(average_price(region_postings))
#         print 'average year: %s' % average_year(region_postings)
# 
#         # add this region's postings to all postings
#         all_postings.extend(region_postings)
# 
#     # Print summary analysis for all regions processed
#     print '\n*** ALL POSTINGS ***:'
#     print '%s postings retrieved' % len(all_postings)
#     print 'average price: $%s' % "{:,}".format(average_price(all_postings))
#     print 'average year: %s' % average_year(all_postings)

