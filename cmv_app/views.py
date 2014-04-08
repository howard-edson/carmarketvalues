from django.shortcuts import render
from django.views.generic import ListView, DetailView
#from .models import Link, UserProfile
#from .forms import UserProfileForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse,reverse_lazy
from cmv_app.models import Search
from cmv_app.forms import SearchForm

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
    


    

#Not implemented
# class UserProfileDetailView(DetailView):
#     """
#     userprofile view - not implemented yet
#     """
#     model = get_user_model()
#     slug_field = "username"
#     template_name = "user_detail.html"
# 
#     def get_object(self, queryset=None):
#         user = super(UserProfileDetailView, self).get_object(queryset)
#         UserProfile.objects.get_or_create(user=user)
#         return user
# 
# class UserProfileEditView(UpdateView):
#     model = UserProfile
#     form_class = UserProfileForm
#     template_name = "edit_profile.html"
# 
#     def get_object(self, queryset=None):
#         return UserProfile.objects.get_or_create(user=self.request.user)[0]
# 
#     def get_success_url(self):
#         return reverse("profile", kwargs={"slug": self.request.user})
