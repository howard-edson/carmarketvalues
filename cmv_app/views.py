from django.shortcuts import render, get_object_or_404, get_list_or_404,\
    redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from cmv_app.models import Search, Posting, BookMark
from cmv_app.forms import SearchForm, SortFieldsForm
from django.db.models import Avg, Count, Max, Min
from django.core.urlresolvers import reverse,reverse_lazy
from cmv_app.models import Search, Region, Posting
from cmv_app.forms import SearchForm, SearchInputForm, SearchCreateForm,\
    SearchUpdateForm
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib import messages
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from cmv_app.shortcuts import populate_one_search, MODELS_MAKE
from django.utils import simplejson
from django.core.exceptions import PermissionDenied



class SearchListView(ListView):
    """
    displays the saved searches of a user in a list view    
    """
    model = Search
    paginate_by = 5
    
    def get_queryset(self):
        return Search.objects.filter(user=self.request.user.id)
    

class PostingsDetailView(DetailView):
    model=Posting
    context_object_name='post'
    
    def get_context_data(self,**kwargs):
        context=super(DetailView,self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            bookmarks=BookMark.objects.filter(post=self.object)
            context["bookmarks"] = bookmarks
        return context
    
class PostingsListView(ListView):
    model=Posting
    template_name="cmv_app/search_detail.html"
    context_object_name="posts"
    pk=None
        
    def get_queryset(self):   
        self.pk=self.kwargs.get('pk',None)
        posts=Posting.objects.filter(search__pk=self.pk)
        region=self.kwargs.get('region',None)
        if region:
            posts=posts.filter(region__name=region)
        return posts
    
    def get_context_data(self,**kwargs):
        context=super(PostingsListView,self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            requested_search=Search.objects.get(pk=self.pk)
            context['currentuser']=requested_search.user
            context['search_pk']=self.pk
            context['search']=requested_search
            form=SortFieldsForm()
            context['form']=form
            context['region']=self.kwargs.get('region',None)
        
            bookmarks = BookMark.objects.filter(user=self.request.user)
            posts_in_page = [posting.id for posting in context["posts"]]
            bookmarks = bookmarks.filter(post_id__in=posts_in_page)
            bookmarks = bookmarks.values_list('post_id', flat=True)
            print bookmarks
            context["bookmarks"] = bookmarks
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
        vehicle_make=self.request.POST['vehicle_make']
        vehicle_model=self.request.POST['vehicle_model']
        f = form.save(commit=False)
        f.user = self.request.user
        f.vehicle_make=vehicle_make
        f.vehicle_model=vehicle_model
        f.save()
        f.regions=form.cleaned_data['regions']
        f.save()
        
        if form.cleaned_data['submit_button_type'] == 'submit_and_add':
            self.success_url = reverse_lazy("search_create")
        messages.add_message(self.request, messages.SUCCESS,
                                 "search saved succcessfully")
        populate_one_search(f)
        return super(SearchCreateView, self).form_valid(form)
    

class SearchUpdateView(SuccessMessageMixin,UpdateView):
    """
    updates an existing saved search of the user
    """
    model = Search
    form_class = SearchUpdateForm
    success_message="succcesfully updated"
    
    success_url = reverse_lazy("searchhome")
    
    def form_valid(self, form):
        f = form.save(commit=False)
        vehicle_make=self.request.POST['vehicle_make']
        vehicle_model=self.request.POST['vehicle_model']
        f.user = self.request.user
        f.vehicle_make=vehicle_make
        f.vehicle_model=vehicle_model
        f.regions=form.cleaned_data['regions']
        Posting.objects.filter(search__pk=f.id).delete()
        f.save()
        populate_one_search(f)
        return super(SearchUpdateView, self).form_valid(form)
    
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SearchUpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

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
            raise PermissionDenied
        return obj
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SearchDeleteView, self).delete(request, *args, **kwargs)


def search_report(request, pk):
    # display a summary report for a search
    rows = []
    total_postings = 0
    search = get_object_or_404(Search, pk=pk)
    regions = search.regions.all()
    for r in regions:
        # build a row for the report (one row per region)
        row = dict()
        row['region'] = r
        postings = Posting.objects.filter(search=pk, region=r)
        count = len(postings)
        total_postings += count
        if postings.exists():
            row['postings_count'] = count
            row['postings_oldest'] = postings.aggregate(Min('last_updated'))['last_updated__min']
            row['postings_newest'] = postings.aggregate(Max('last_updated'))['last_updated__max']            
            row['year_avg'] = int(postings.aggregate(Avg('vehicle_year'))['vehicle_year__avg'])
            row['year_min'] = postings.aggregate(Min('vehicle_year'))['vehicle_year__min']
            row['year_max'] = postings.aggregate(Max('vehicle_year'))['vehicle_year__max']
            row['price_avg'] = int(postings.aggregate(Avg('vehicle_price'))['vehicle_price__avg'])
            row['price_min'] = postings.aggregate(Min('vehicle_price'))['vehicle_price__min']
            row['price_max'] = postings.aggregate(Max('vehicle_price'))['vehicle_price__max']
        rows.append(row)
    context = {'search': search, 'rows': rows, 'total_count': total_postings}
    return render(request, 'cmv_app/search_report.html', context)


class SearchListJson(BaseDatatableView):
    model = Search

    columns=['title','created','min_price', 'max_price','actions']
    order_columns = ["title",'created', 'min_price','max_price',"actions"]
    max_display_length = 500

    def render_column(self, row, column):
        url_edit=static('images/icons/icon_changelink.gif')
        url_delete=static('images/icons/icon_deletelink.gif')
        
        
        if column == 'title':
            regions= row.regions.all() 
            if len(regions)==1:
                 value = '{0} => {1}:{2}-{3}-{4}'.format(row.vehicle_make,row.vehicle_model,
                                           row.max_year,row.min_year,regions[0].name.title())
                 edit_url = reverse('postings_list_regions', 
                                    kwargs={'pk':row.id,'region':regions[0]})
                 return self.get_value_cell_style(edit_url, value,'red')
            else:
                value = '{0} => {1}:{2}-{3}'.format(row.vehicle_make,row.vehicle_model,
                                           row.max_year,row.min_year)
                reg=""
                for link in regions:
                    url=reverse('postings_list_regions',
                                kwargs={'pk':row.id,'region':link.name})
                    reg+='''<li><a href="%s">%s</a></li>'''%(url,link.name.title())
                dropdownHtml=  '''
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                    &nbsp;%s <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu regions-dropdown">
                    %s </ul>'''%(value,reg)            
                return dropdownHtml
        
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
    

def get_makes_json(request,make):
    if not request.is_ajax():
            return HttpResponse("you cant access here")
    models=MODELS_MAKE.get(make,None)
    if models:
        results=tuple(models)
        obj=simplejson.dumps(results)
        return HttpResponse(obj, content_type="application/json")
    
    
def bookmark_post(request): 
    if not request.is_ajax():
        return HttpResponse("you cant access here")
    post_id=request.POST['id']
    ret = {"success": 0}
    try:
        bookmark = BookMark.objects.get(post__pk=post_id)
    except BookMark.DoesNotExist:
        BookMark.objects.create(user=request.user,post=Posting.objects.get(pk=post_id))
        #success if new bookmark is created
        ret['success']=1
    else:
        BookMark.delete(bookmark)
    return HttpResponse(simplejson.dumps(ret), content_type="application/json")


class BookMarkListView(ListView):
      
    model=BookMark
    template_name="cmv_app/bookmark_list.html"
    context_object_name='bookmarks'
      
      
    def get_queryset(self):
        return BookMark.objects.filter(user=self.request.user.id).order_by('-created')
    

def unbookmark(request):
    bm_id=request.POST.get("bookmark_id",None)
    if bm_id:
        bookmark = BookMark.objects.get(post__pk=bm_id)
        BookMark.delete(bookmark)
    return redirect('bookmark_listView')

    
    
    
    
    

