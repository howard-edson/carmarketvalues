from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
#from .models import Link, UserProfile
#from .forms import UserProfileForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from cmv_app.models import Search, Posting
from cmv_app.forms import SearchForm
from django.db.models import Avg, Count

class SearchListView(ListView):
    """
    displays the saved searches of a user in a list view    
    """
    model = Search
    #queryset = Search.objects.filter(user=request.user)
    paginate_by = 5
    
    def get_queryset(self):
        return Search.objects.filter(user=self.request.user)
    

class SearchDetailView(DetailView):
    model=Search
    

class SearchCreateView(CreateView):
    """
    displays form to create a new search
    """
    model = Search
    form_class = SearchForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.rank_score = 0.0
        f.submitter = self.request.user
        f.save()
        return super(SearchCreateView, self).form_valid(form)

class SearchUpdateView(UpdateView):
    """
    updates an existing saved search of the user
    """
    model = Search
    form_class = SearchForm
    
    success_url = reverse_lazy("home")

class SearchDeleteView(DeleteView):
    """
    deletes saved search of the user
    """
    model = Search
    success_url = reverse_lazy("home")
    

def search_report(request, pk):
    # display detail for a particular search
    context = {}
    search = get_object_or_404(Search, pk=pk)
    context['search'] = search
    postings = Posting.objects.filter(search=pk)
    if postings.exists():
        context['postings_count'] = len(postings)
        context['x'] = postings.values('region__name').annotate(
            year=Avg('vehicle_year'),
            price=Avg('vehicle_price'),
            tcount=Count('title'),
        )

        return render(request, 'cmv_app/search_report.html', context)
    else:
        pass
        # return 404!
    
