import datetime
from .models import TimeKeeper, Artists
from . import get_concert_data as gcd

def main():
    today = datetime.date.today()
    tk = TimeKeeper.objects.filter(id=4)[0]
    last_concert_search = tk.last_date
    
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
        #below code should delete old concerts that have already happened
        concerts = Artists.objects.all()
        for concert in concerts:
            concert_id = concert.id
            concert_date = concert.date
            concert_date_object = datetime.datetime.strptime(concert_date, '%m%d%Y')
            if today > concert_date_object.date():
                Artists.objects.filter(id=concert_id).delete()
            
    
    
    
