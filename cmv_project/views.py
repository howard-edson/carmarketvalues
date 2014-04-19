from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy
from cmv_project import settings
from django.views.generic.edit import FormView
from cmv_project.forms import UserSettingsForm
from django.contrib import messages



class HomePageView(TemplateView):
    
    template_name="home.html"
    
def user_login(request):
    # Force logout.
    #logout(request)
    username = password = ''

    # Flag to keep track whether the login was invalid.
    login_failed = False

    if request.POST:
        username = request.POST['username'].replace(' ', '').lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                rememberMe(request)
                return HttpResponseRedirect(reverse('searchhome'))
        else:
            login_failed = True

    return render(request,'home.html',
                              {'login_failed': login_failed})
    

def rememberMe(request):
    if not request.POST.get('remember_me',None):
        request.session.set_expiry(0)
        
        
class UserSettingsView(FormView):
    #success_url = reverse_lazy('searchhome')
    form_class = UserSettingsForm
    template_name = 'usersettings.html'

    def get_initial(self):
        user = self.request.user
        

        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        
    def get_success_url(self):
        return reverse('searchhome')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Settings Saved!')

        return super(UserSettingsView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():
            user = self.request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
