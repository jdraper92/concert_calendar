from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import pickle
#from .models import User
#from django import forms

#so you're gonna need to check if the username exists and if it does if it's time to update
#if only one or neither are true then you need to display the url to go to and have the user go there.
#then the user can go there by clicking the link and having it open in a new tab/window.
#but how do you keep the app running during this time? I think you could keep it waiting in the code
#function in views.py and then have the code finish and display the concerts from there. 
from . import spotipygetplayliststest as sgp

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
    if not username or not email:
        return HttpResponseRedirect(reverse('muscal:index'))
    spotify_obj = sgp.GetPlaylists(username,email)
    user_existence = spotify_obj.doesUserExist()
    if user_existence:
        concerts = spotify_obj.getConcerts()
        return render(request,'plist_concerts/after.html',{'concerts': concerts})
    else:
        auth_url = spotify_obj.getUrl()
        pickle_out = open("spotify.pickle","wb")
        pickle.dump(spotify_obj, pickle_out)
        pickle_out.close()
        return render(request,'plist_concerts/code.html',{'auth_url': auth_url})
        
    #error check to make sure user put in all info
##    if not username or not email:
##        return HttpResponseRedirect(reverse('muscal:index'))
##    #(concerts,run_check,need_code) = sgp.main(username,email)
##    url = sgp.getUrl(username,
##
##    return render(request,'plist_concerts/code.html',{'concerts': concerts})

def code(request, c):
    pickle_in = open("spotify.pickle","rb")
    spotify_obj = pickle.load(pickle_in)
    (concerts,check) = spotify_obj.tokenReceived(c)
    if not check:
        return HttpResponseRedirect(reverse('muscal:error'))
    #return render(request,'plist_concerts/code.html', {'c' : c})
    return render(request,'plist_concerts/after.html',{'concerts': concerts})

def done(request):
    #u = User.objects.get(user_name = use)
    #return render(request,'spotify/after.html', {'user' : user, 'time': u.time_frame, 'songs': u.num_songs})
    return render(request,'plist_concerts/after.html')

def error(request):
    return render(request, 'plist_concerts/error.html')
