# shows a user's playlists (need to be authenticated via oauth)
import os
import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import datetime
from .models import User, TimeKeeper, Artists
from . import get_concert_data as gcd
from . import add_concerts_to_db as actb
import json
from rq import Queue
from .worker import conn
from .auth import goToSpotify

lock = True
code = None
class GetPlaylists():
    def __init__(self,username,email):
        self.username=username
        self.email = email
        self.client_id= os.environ['SPOTIPY_CLIENT_ID']
        self.client_secret =os.environ['SPOTIPY_CLIENT_SECRET']
        self.redirect_uri =os.environ['SPOTIPY_REDIRECT_URI']
        self.sp_oauth = oauth2.SpotifyOAuth(self.client_id, self.client_secret, self.redirect_uri, 
        scope=None, cache_path=None)
        
    def make_artist_list(self,tracks):
        artist_list = []
        for i, item in enumerate(tracks['items']):
            track = item['track']
            artist_list += [track['artists'][0]['name']]
        return artist_list


    def grabPlaylists(self,token):
        scope = ''
        artists = []
        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(self.username)
        else:
            #ADD SOMETHING HERE
            return []

        for playlist in playlists['items']:
                try:
                    if playlist['owner']['id'] == self.username:
                        results = sp.user_playlist(self.username, playlist['id'],
                            fields="tracks,next")
                        tracks = results['tracks']
                        temp = self.make_artist_list(tracks)
                        artists += self.make_artist_list(tracks)
                        while tracks['next']:
                            tracks = sp.next(tracks)

                            temp = self.make_artist_list(tracks)

                            artists += self.make_artist_list(tracks)
                except UnicodeEncodeError:
                    continue
        artists = set(artists)
        artists = list(artists)
        return artists
        
    def getUrl(self):
        token_info = False
        auth_url = self.sp_oauth.get_authorize_url()
        return auth_url

    def tokenReceived(self,code):
        c = self.sp_oauth.parse_response_code(self.redirect_uri + '/?code=' + str(code)) #DOES THIS NEED TO CHANGE WITH FINAL COMMIT?
        token_info = self.sp_oauth.get_access_token(c)
        token = token_info['access_token']
        self.getSpotifyPlaylists(token)
        concerts = self.getConcerts()
        return (concerts,True)
        
    def getSpotifyPlaylists(self,token):
        today = datetime.date.today()
        if User.objects.filter(username = self.username).exists():
            returning_user = User.objects.filter(username = self.username)[0]
            artists = self.grabPlaylists(token)
            today = datetime.date.today()
            returning_user.artists = json.dumps(artists)
            returning_user.last_update = today.strftime('%m%d%Y') #changed to strftime from strptime
            returning_user.save()
        else:
            artists = self.grabPlaylists(token)
            last_update = today.strftime('%m%d%Y') #changed
            user = User(username = self.username, artists = json.dumps(artists),email = self.email, last_update = last_update)
            user.save()

    def doesUserExist(self):
        today = datetime.date.today()
        returning_user = User.objects.filter(username = self.username).exists()
        if returning_user:
            returning_user = User.objects.filter(username = self.username)[0]
            last_update = datetime.datetime.strptime(returning_user.last_update, '%m%d%Y')
            if today <  last_update.date() + datetime.timedelta(days=30):#This is only true if today's date is less than 30 days past last update 
                return True

        return False

    def getConcerts(self):
        returning_user = User.objects.filter(username = self.username)[0]
        jsonDec = json.decoder.JSONDecoder()
        artists = jsonDec.decode(returning_user.artists)
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
        return matches_list2

    
