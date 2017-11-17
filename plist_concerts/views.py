from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
#from .models import User
#from django import forms
import spotipygetplayliststest as sgp

# Create your views here
def index(request):
    c = request.GET.get('code', False)
    if c != False:
        return code(request, c)
    else:
        #you don't need to include a dictionary
        return render(request, 'plist_concerts/index.html')

def submit(request):
    username = request.POST.get('user', False)
    email = request.POST.get('email', False)

    #error check to make sure user put in all info
    if not username or not email:
        return HttpResponseRedirect(reverse('muscal:index'))

    (concerts,run_check) = sgp.main(username,email)

    if not run_check:
        return HttpResponseRedirect(reverse('muscal:error'))

    return render(request,'plist_concerts/after.html',{'concerts': concerts})

def code(request, c):
    sgp.getToken(c)
    return render(request,'plist_concerts/code.html', {'c' : c})

def done(request):
    #u = User.objects.get(user_name = use)
    #return render(request,'spotify/after.html', {'user' : user, 'time': u.time_frame, 'songs': u.num_songs})
    return render(request,'plist_concerts/after.html')

def error(request):
    return render(request, 'plist_concerts/error.html')
