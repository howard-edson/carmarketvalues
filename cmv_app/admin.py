from django.contrib import admin
from cmv_app.models import Region, Search, Posting, BookMark
#this is brand new
from .models import Region, Search, Posting
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class PostingInline(admin.StackedInline):
    model=Posting.search.through  # @UndefinedVariable

class SearchAdmin(admin.ModelAdmin):
    inlines=(PostingInline,)
    list_display = ('id', 'user', 'created', 'vehicle_make', 'vehicle_model',
                    'extra_keywords', 'max_price', 'min_price', 'max_year',
                    'min_year')

    list_filter = ['user']
    
class PostingAdmin(admin.ModelAdmin):
    
    list_display = ('id','posting_url', 'region', 'last_updated', 
                    'title')

    list_filter = ['region']
    
class SearchInline(admin.TabularInline):
     model=Search
     
class MyUserAdmin(UserAdmin):
    inlines=(SearchInline,)
    
    
    
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(Region)
admin.site.register(Search, SearchAdmin)
admin.site.register(Posting, PostingAdmin)
admin.site.register(BookMark)
