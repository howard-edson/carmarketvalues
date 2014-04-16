from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse



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
                return HttpResponseRedirect(reverse('searchhome'))
        else:
            login_failed = True

    return render(request,'home.html',
                              {'login_failed': login_failed})
