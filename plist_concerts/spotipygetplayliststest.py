# shows a user's playlists (need to be authenticated via oauth)
import os
import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import webbrowser
import datetime
from .models import User, TimeKeeper, Artists
from . import get_concert_data as gcd
from . import add_concerts_to_db as actb
import json

lock = True
code = None

def make_artist_list(tracks):
    artist_list = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        artist_list += [track['artists'][0]['name']]
    return artist_list


def getPlaylists(username):
    scope = ''
    artists = []

    token = util_new(username)
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
    else:
        #ADD SOMETHING HERE
        return []

    for playlist in playlists['items']:
            try:
                if playlist['owner']['id'] == username:
                    results = sp.user_playlist(username, playlist['id'],
                        fields="tracks,next")
                    tracks = results['tracks']
                    temp = make_artist_list(tracks)
                    artists += make_artist_list(tracks)
                    while tracks['next']:
                        tracks = sp.next(tracks)

                        temp = make_artist_list(tracks)

                        artists += make_artist_list(tracks)
            except UnicodeEncodeError:
                continue
    artists = set(artists)
    artists = list(artists)
    return artists

def util_new(username, scope=None, client_id = None,client_secret = None, redirect_uri = None):
    client_id= os.environ['SPOTIPY_CLIENT_ID']
    client_secret =os.environ['SPOTIPY_CLIENT_SECRET']
    redirect_uri =os.environ['SPOTIPY_REDIRECT_URI']
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
    scope=scope, cache_path=None)
    token_info = False

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        ##        q = Queue(connection=conn)
        ##        job = q.enqueue(webbrowser.open, auth_url)
        #goToSpotify(auth_url)
        webbrowser.open(auth_url)
        global lock
        while lock:
            c = 1
            #infinite loop motherfucker

        c = sp_oauth.parse_response_code(os.environ['SPOTIPY_REDIRECT_URI'] + '/?code=' + str(code)) #DOES THIS NEED TO CHANGE WITH FINAL COMMIT?

        token_info = sp_oauth.get_access_token(c)
        # Auth'ed API request
        if token_info:
            return token_info['access_token']
        else:
            return None

    else:
        return token_info['access_token']

def getToken(c):
    global code
    code = c
    global lock
    lock = False

def main(username,email):
    print('here111111')
    #actb.main() don't want to call this for everyone because it takes too long
    returning_user = User.objects.filter(username = username).exists()
    today = datetime.date.today()

    if returning_user:
        print('here222222')
        returning_user = User.objects.filter(username = username)[0]
        jsonDec = json.decoder.JSONDecoder()

        last_update = datetime.datetime.strptime(returning_user.last_update, '%m%d%Y')
        if today> last_update.date() + datetime.timedelta(days=30):#This is only true if today's date is further in the future than last_update + 30 days aka hasn't been updated in over 30 days

            artists = getPlaylists(returning_user.username)
            returning_user.artists = json.dumps(artists)
            returning_user.last_update = today.strftime('%m%d%Y') #changed to strftime from strptime
            returning_user.save()
        else:
            print('here33333')
            artists = jsonDec.decode(returning_user.artists)
    else:
        artists = getPlaylists(username)
        last_update = today.strftime('%m%d%Y') #changed
        user = User(username = username, artists = json.dumps(artists),email = email, last_update = last_update)
        user.save()
    matches = {}
    for artist in artists:
        try:
            a = Artists.objects.filter(name = artist)
            location = str(a[0].location)
            date = a[0].date 
            if date in matches:
                 matches[date] += [(artist,location)]
            else:
             matches[date] = [(artist,location)]
        except (KeyError,AttributeError,IndexError):
            continue
    print('here444444')
    matches_list = []
    for key in matches:
        for concert in matches[key]:
            (a,l) = concert
            d = datetime.datetime.strptime(key, '%m%d%Y') # changed #have to convert to date object to sort them
            matches_list += [(d,a,l)]
            matches_list = sorted(matches_list)
            matches_list2 = []
    for x in matches_list:
        (d,a,l) = x
        matches_list2 += [(d.strftime('%m%d%Y'),a,l)]
    return (matches_list2, True)



    
