import datetime
from models import TimeKeeper
import get_concert_data as gcd

def main():
    today = datetime.date.today()
    tk = TimeKeeper.objects.filter(id=4)[0]
    last_concert_search = tk.last_date
    last_concert_search = datetime.datetime.strptime(last_concert_search, '%m%d%Y')
    if today > last_concert_search.date():
        b = gcd.BandInfo()
        for x in range(0,120):
            date = last_concert_search.strftime('%m%d%Y') #changed
            b.makeDict(date)
            last_concert_search = last_concert_search + datetime.timedelta(days=1)
        #below code is how we update the reference time that we will use to search for concerts
        #in the future. So next time we start from today + 
        today = datetime.date.today()
        reference = today + datetime.timedelta(days=75)
        new_last_date = reference.strftime('%m%d%Y') 
        tk.last_date = new_last_date
        tk.save()
    
    
    
