from django.db import models
from django.contrib.auth.models import User

# Note: Users will be stored in django's automatically-created users table

class Website(models.Model):
    """
    A website we search for postings. The domain is used in constructing 
    the search url. In v1.0 our only record in this table is 'craigslist.org'
    
    """
    domain = models.CharField(max_length=100, unique=True, 
        help_text="the part of the website used in constructing urls")

    def __unicode__(self):
        return self.domain


class Region(models.Model):
    """
    The geographic region specified for a search, and in which a posting was read.
    When constructing a url, the region name prepends craigslist.org.
    For example 'seattle.craigslist.org/?...'
    
    """
    name = models.CharField(max_length=100, verbose_name="region name", unique=True,
        help_text="prepends craigslist.org when constructing urls")

    def __unicode__(self):
        return self.name


class Search(models.Model):
    """
    A Search is created by a user, and run daily, collecting new postings each day.
    A user may define his search to run in one or more regions 
    (e.g. Atlanta and Portland).
    
    """
    
    SELLER_TYPE_CHOICES = (
        ('o', 'Private Owner'),
        ('d', 'Dealer'),
        ('a', 'All'),
    )
    
    user = models.ForeignKey(User)
    region = models.ManyToManyField(Region, related_name='s_r+')  # one search runs in many regions
    vehicle_make = models.CharField(max_length=100, blank=True)
    vehicle_model = models.CharField(max_length=100, blank=True)
    extra_keywords = models.CharField(max_length=100, blank=True)
    max_price = models.PositiveIntegerField(null=True, blank=True)
    min_price = models.PositiveIntegerField(null=True, blank=True)
    max_year = models.PositiveIntegerField(null=True, blank=True)
    min_year = models.PositiveIntegerField(null=True, blank=True)
    pic_only = models.BooleanField(help_text="only find postings with pics")
    search_title_only = models.BooleanField(help_text="only search posting titles")
    seller_type = models.CharField(max_length=1, choices=SELLER_TYPE_CHOICES, default="a")

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.vehicle_make, self.vehicle_model, self.extra_keywords)

    class Meta:
        verbose_name_plural = "searches"


class Posting(models.Model):
    """
    A Posting (listing) is returned when a search is run. Two or more searches
    could conceivably return the same posting, so we have the many-to-many
    relationship implemented here.
    
    """
    website = models.ForeignKey(Website)
    region = models.ForeignKey(Region)
    # A posting may be associated with more than one search
    search = models.ManyToManyField(Search, related_name='p_s+')
    # prevents duplicate postings
    website_posting_id = models.CharField(max_length=100, unique=True)
    last_updated = models.DateField(auto_now=True)
    vehicle_year = models.PositiveIntegerField(null=True, blank=True)
    vehicle_price = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name="posting title")
    body = models.TextField(verbose_name="posting body text")

    def __unicode__(self):
        return "{0} ({1})".format(self.title, self.last_updated)
