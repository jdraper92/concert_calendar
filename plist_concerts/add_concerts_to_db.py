import datetime
from .models import TimeKeeper, Artists
from . import get_concert_data as gcd
import threading
            
class concertThreads(threading.Thread):
    def __init__(self,threadID, name,start,last_day,cleanDB):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.starting_pos = start #starting date
      self.iter = 4 #number of days to check
      self.last_day = last_day +  datetime.timedelta(days=start) #I think this is right
      self.cleanDB = cleanDB
    def run(self):
        if self.cleanDB:
            concerts = Artists.objects.all()
            today = datetime.date.today()
            for concert in concerts:
                concert_id = concert.id
                concert_date = concert.date
                concert_date_object = datetime.datetime.strptime(concert_date, '%m%d%Y')
                if today > concert_date_object.date():
                    Artists.objects.filter(id=concert_id).delete()
        else:
            b = gcd.BandInfo()
            for x in range(self.starting_pos,self.starting_pos + self.iter):
                date = self.last_day.strftime('%m%d%Y') #changed
                b.makeDict(date)
                self.last_day +=  datetime.timedelta(days=1)
    
def main():
    today = datetime.date.today()
    tk = TimeKeeper.objects.filter(id=4)[0]
    last_concert_search = tk.last_date
    today = today.strftime('%m%d%Y')
    today = datetime.datetime.strptime(today, '%m%d%Y')
    last_day = datetime.datetime.strptime(last_concert_search, '%m%d%Y')
    last_accessed = datetime.datetime.strptime(tk.last_accessed, '%m%d%Y')
    if today > last_accessed + datetime.timedelta(days=14):#we will update the concerts every 2 weeks
        threadA = concertThreads(1,'1',0,last_day,False)
        threadB = concertThreads(2,'2',4,last_day,False)
        threadC = concertThreads(3,'3',8,last_day,False)
        threadE = concertThreads(5,'5',12,last_day,False)
        threadD = concertThreads(4,'4',0,last_day,True) #cleans up the db
        threadA.start()
        threadB.start()
        threadC.start()
        threadD.start()
        threadE.start()

        threadA.join()
        threadB.join()
        threadC.join()
        threadD.join()
        threadE.join()
        #below code is how we update the reference time that we will use to search for concerts
        #in the future. So next time we start from today + 
        today = datetime.date.today()
        reference = last_day + datetime.timedelta(days=40)
        new_last_date = reference.strftime('%m%d%Y') 
        tk.last_date = new_last_date
        tk.last_accessed = today.strftime('%m%d%Y') 
        tk.save()
    else:
        threadD = concertThreads(4,'4',0,last_day,True)
        threadD.start()
        threadD.join()

    
