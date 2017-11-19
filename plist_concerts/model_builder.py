import os
import sys
from bs4 import BeautifulSoup
import urllib2
import datetime
from .models import Artists, TimeKeeper
from . import get_concert_data as gcd

today = datetime.date.today()
dates = []
tk = TimeKeeper(first_date=today.strftime('%m %d %Y'), last_date=today + datetime.timedelta(days=180))
for x in range(0,180):
   dates += [today.strftime('%m %d %Y')]
   today = today + datetime.timedelta(days=1)
#concert_data = {} # you want one hash table with all of the concert data so you have to keep passing in each updated version of it
b = gcd.BandInfo()
concert_data = {}
for date in dates:
    concert_data.update(b.makeDict(date))
