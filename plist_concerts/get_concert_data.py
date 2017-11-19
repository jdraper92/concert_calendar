from bs4 import BeautifulSoup
import urllib3
import datetime
from .models import Artists,TimeKeeper

class BandInfo:
    def __init__(self):
        self.raw_date = '' #should be 11 22 2016 format (mon day year)
        self.day = ''
        self.month = ''
        self.year = ''
        self.formatted_date = ''
        self.hash_table = {}

    #builds the url with proper date and constructs the formatted date used later to search the soup
    def makeUrl(self):
        months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August',\
         '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
        days_of_week = {0:'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'} 

        split_date = self.raw_date.split(' ') #month, day, year
        url = 'http://www.songkick.com/metro_areas/9426-us-chicago?utf8=%E2%9C%93&filters%5BminDate%5D=' + self.month + '%2F' + self.day + '%2F' + self.year + '&filters%5BmaxDate%5D=' + self.month + '%2F' + self.day + '%2F' + self.year + '#date-filter-form'
        self.formatted_date = datetime.datetime.strptime(self.raw_date, '%m%d%Y')
        wk_day = days_of_week[self.formatted_date.weekday()] #returns the int of what day it is in 0-6 format where 0 is mondaythen put in as dict ke
        self.formatted_date = wk_day + ' ' + self.day + ' ' + months[self.month] + ' ' + self.year #makes date of the form Tuesday 22 November 2016
        return url

    #returns a tuple with each band/concert location for that day
    def getFromSongkick(self):
        url = self.makeUrl()
        #page = urllib2.urlopen(url).read()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data)
        try:
            test = soup.find(text = self.formatted_date)
            locations = test.findAllNext('span', attrs = {'class': ['location'], 'class': ['venue-name']})
            bands = test.findAllNext('strong')
        except AttributeError:
            bands = []
            locations = []
            
        bands_str = []
        locations_str = []
        
        for band in bands:
            try:
                band = str(band)
                band = band.split('<strong>')
                band = band[1].split('</strong>')
                bands_str += [band[0]]
            except IndexError:
                continue
        for location in locations:
            try:
                location = str(location)
                location = location.split('</a></span>')
                location = location[0].split('>')
                locations_str += [location[len(location) - 1]]
            except IndexError:
                continue
        return zip(bands_str, locations_str)
    
    #makes a hashable table of the given day's concerts
    def makeDict(self,date):
        self.raw_date = date
        self.month = date[0:2]
        self.day = date[2:4]
        self.year = date[4:8]
        bands_and_locations = self.getFromSongkick()
        for (band,loc) in bands_and_locations:
            if Artists.objects.filter(name = band).exists():
                continue
            else:
                artist = Artists(name=band, location=loc, date=date)
                artist.save()
        return True





