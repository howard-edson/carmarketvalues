from django.contrib import admin
from cmv_app.models import Region, Search, Posting

class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'vehicle_make', 'vehicle_model',
                    'extra_keywords', 'max_price', 'min_price', 'max_year',
                    'min_year')

    list_filter = ['user']

class PostingAdmin(admin.ModelAdmin):
    list_display = ('posting_url', 'region', 'last_updated', 
                    'title')

    list_filter = ['region']

admin.site.register(Region)
admin.site.register(Search, SearchAdmin)
admin.site.register(Posting, PostingAdmin)