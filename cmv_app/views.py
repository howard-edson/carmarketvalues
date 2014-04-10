from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Search, Posting

def index(request):
#     TODO:
#     If not signed in:
#         sign in or register
#     else:
#         display my searches (redirect?)
    context = {}
    return render(request, 'cmv_app/index.html', context)


# def my_searches(request):
#     # display all searches
#     # TODO: limit to just the current user's searches
#     searches = Search.objects.all()
#     context = {'searches': searches}
#     return render(request, 'cmv_app/search_summary.html', context)


def search_detail(request, search_id):
    # display detail for a particular search
    search = get_object_or_404(Search, pk=search_id)
    return render(request, 'cmv_app/search_detail.html', {'search': search})


def search_new(request):
    context = {}
    return render(request, 'cmv_app/search_new.html', context)


def search_delete(request, search_id):
    return HttpResponse("search_delete for search {}".format(search_id))


def search_report(request, search_id):
    context = {'seach_id': search_id}
    return render(request, 'cmv_app/search_report.html', context)
#########################################################################
# A class-based generic view to display all searches
class SearchList(ListView):
    model = Search
    context_object_name = 'search_list'
    template_name = 'cmv_app/search_list.html'
    #TODO - filter this to only show the signed-in user's Searches.
    queryset = Search.objects.all()

class PostingList(ListView):
    model = Posting
    context_object_name = 'posting_list'
    template_name = 'cmv_app/search_report.html'
    queryset = Posting.objects.all()
