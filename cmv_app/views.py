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
from django.core.urlresolvers import reverse,reverse_lazy
from cmv_app.models import Search, Region, Posting
from cmv_app.forms import SearchForm, SearchInputForm, SearchCreateForm,\
    SearchUpdateForm
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib import messages
from django.http.response import Http404
from django.contrib.messages.views import SuccessMessageMixin

class SearchListView(ListView):
    """
    displays the saved searches of a user in a list view    
    """
    model = Search
    #queryset = Search.objects.filter(user=request.user)
    paginate_by = 5
    
    def get_queryset(self):
        return Search.objects.filter(user=self.request.user.id)
    

class PostingsListView(ListView):
    model=Posting
    template_name="cmv_app/search_detail.html"
    context_object_name="posts"
    pk=None
        
    def get_queryset(self):
        self.pk=self.kwargs.get('pk',None)
        posts=Posting.objects.filter(search__pk=self.pk)
        return posts
    
    def get_context_data(self,**kwargs):
        context=super(PostingsListView,self).get_context_data(**kwargs)
        requested_search=Search.objects.get(pk=self.pk)
        context['currentuser']=requested_search.user
        context['search_pk']=self.pk
        context['search']=requested_search
        return context
        
class SearchCreateView(CreateView):
    """
    displays form to create a new search
    """
    model = Search
    form_class = SearchCreateForm
    
    success_url = reverse_lazy('searchhome')
    template_name = 'cmv_app/search_form.html'

    def form_valid(self, form):
        f = form.save(commit=False)
        region=self.request.POST['region']
        f.user = self.request.user
        f.save()
        f.regions.add(Region.objects.get(name=region))
        if form.cleaned_data['submit_button_type'] == 'submit_and_add':
            self.success_url = reverse_lazy("search_create")
        messages.add_message(self.request, messages.SUCCESS,
                                 "search successfully saved. You may \
                                 add another.")
        return super(SearchCreateView, self).form_valid(form)

class SearchUpdateView(UpdateView):
    """
    updates an existing saved search of the user
    """
    model = Search
    form_class = SearchUpdateForm
    
    success_url = reverse_lazy("searchhome")

class SearchDeleteView(DeleteView):
    """
    deletes saved search of the user
    """
    model = Search
    success_url = reverse_lazy("searchhome")
    success_message="succcesfully deleted"

    def get_object(self,queryset=None):
        """
        make sure object is owned by currently logged in user
        """
        obj=super(SearchDeleteView,self).get_object()
        if not obj.user==self.request.user:
            raise Http404
        return obj
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SearchDeleteView, self).delete(request, *args, **kwargs)


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

class SearchListJson(BaseDatatableView):
    model = Search

    columns=['title','created','min_price', 'max_price','actions']
    order_columns = ["title",'created', 'min_price','max_price',"actions"]
    max_display_length = 500

    def render_column(self, row, column):
        url_edit=static('images/icons/icon_changelink.gif')
        url_delete=static('images/icons/icon_deletelink.gif')

        if column == 'title':
             value = '{0}=>{1}:{2}-{3}'.format(row.vehicle_make,row.vehicle_model,
                                           row.max_year,row.min_year)
             edit_url = reverse('postings_list', args=(row.id,))
             return self.get_value_cell_style(edit_url, value,'red')

        if column == 'max_price':
            return '%s' %row.max_price
        elif column == 'min_price':
             return '%s' %row.min_price
        elif column == 'created':
             return row.created.strftime('%m/%d/%Y')
        elif column == 'actions':
             edit_link = """<a href='%s'><img src='%s'></a>""" %(\
                 reverse('search_update', args=(row.id,)),url_edit)
             delete_link = """<a href='%s'><img src='%s'></a>""" %(\
                 reverse('search_delete', args=(row.id,)),url_delete)
             return '<center>%s&nbsp;%s</center>' % (edit_link, delete_link)
        else:
             return super(SearchListJson, self).render_column(row, column)

    def get_value_cell_style(self, url, value, color=None):
        style = '''<center><a href="%s">%s</a></center>''' % (url, value)
        if color:
            style = '''<center><a href="%s"><font color="%s">%s</font></a>
                </center>''' % (url, color, value)

        return style

    def get_initial_queryset(self):
        """
        Filter records to show only entries from the currently logged-in user.
        """
        return Search.objects.filter(user=self.request.user.id)

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
