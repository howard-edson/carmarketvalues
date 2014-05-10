import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmv_project.settings")

from django.shortcuts import get_object_or_404
from cmv_app.models import Search, Posting
from django.db.models import Avg, Count, Max, Min

def search_report(request, pk):
    # display summary report for a search
    rows = []
    search = get_object_or_404(Search, pk=pk)
    regions = search.regions.all()
    
    for r in regions:
        # build a row for the report (one row per region)
        row = dict()
        row['region'] = r
        postings = Posting.objects.filter(search=pk, region=r)
        if postings.exists():
            row['postings_count'] = len(postings)
            row['postings_oldest'] = postings.aggregate(Min('last_updated'))['last_updated__min']
            row['postings_newest'] = postings.aggregate(Max('last_updated'))['last_updated__max']            
            row['year_avg'] = postings.aggregate(Avg('vehicle_year'))['vehicle_year__avg']
            row['year_min'] = postings.aggregate(Min('vehicle_year'))['vehicle_year__min']
            row['year_max'] = postings.aggregate(Max('vehicle_year'))['vehicle_year__max']
            row['price_avg'] = postings.aggregate(Avg('vehicle_price'))['vehicle_price__avg']
            row['price_min'] = postings.aggregate(Min('vehicle_price'))['vehicle_price__min']
            row['price_max'] = postings.aggregate(Max('vehicle_price'))['vehicle_price__max']
        rows.append(row)
    return rows

if __name__ == '__main__':
    req = None
    rows = search_report(req, 4)
    for row in rows:
        print '\n ** Region: {} **'.format(row['region'])
        print 'postings_count: {}'.format(row['postings_count'])
        print 'postings_oldest: {}'.format(row['postings_oldest'])
        print 'postings_newest: {}'.format(row['postings_newest'])
        print 'year_avg: {}'.format(int(row['year_avg']))
        print 'year_min: {}'.format(row['year_min'])
        print 'year_max: {}'.format(row['year_max'])
        print 'price_avg: ${}'.format(int(row['price_avg']))
        print 'price_min: ${}'.format(int(row['price_min']))
        print 'price_max: ${}'.format(int(row['price_max']))

