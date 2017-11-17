import get_concert_data as gcd
import spotipygetplayliststest as sgp
import datetime

##username = 'jdraper12'
##date = ''
def build_playlist(u,t):
    playlists = sgp.SpotifyPlaylists(u)
    artists = playlists.getPlaylists()
    
##    with open('artists2.txt','w') as ff:
##        for a in artists:
##            ff.write(a)
##            ff.write('\n')
                                  
    today = datetime.date.today()
    dates = []

    for x in range(0,t):
        dates += [today.strftime('%m %d %Y')]
        today = today + datetime.timedelta(days=1)



    #concert_data = {} # you want one hash table with all of the concert data so you have to keep passing in each updated version of it
    b = gcd.BandInfo()
    concert_data = {}
    for date in dates:
        concert_data.update(b.makeDict(date))

    matches = {}
    for key in artists:
        try:
            (l,d) = concert_data[key] #(location,date)
            if d in matches:
                matches[d] += [(key,l)]
            else:
                matches[d] = [(key,l)]
        except KeyError:
            continue

    #for key in matches:
        
##
##    print('')
##    print('')
##    print('')
##    print(matches)
    for key in matches:
        print(key,matches[key] + '\n')

##class BuildPlaylist:
##    def __init__(self,u,t):
##        self.username = u
##        self.timeframe = t


##with open('artists2.txt') as f:
##    artists = [line.rstrip('\n') for line in f]
##
###below code one time thing to remove duplicates
##
##artists = list(set(artists)) #removing duplicates

def sendToken(spotify_object,c):
    spotify_object.getToken(c)
    


