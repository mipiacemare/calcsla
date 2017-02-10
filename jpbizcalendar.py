'''
Created on Feb 10, 2017

@author: inagakii
'''
from datetime import *
SATURDAY = 5
SUNDAY = 6
TZONE_JST='JST'
TZONE_UTC='UTC'

class JpBizCalendar():

    def __init__(self, year, tz):
        self.this_now = datetime.now()
        self.tzone = tz
        self.tzone_conv = True
        self.biz_start_time = 9
        if tz == TZONE_JST:
            self.tzone_conv = False
        self.holiday_2014 = (date(2014,1,1),date(2014,1,13),date(2014,2,11),date(2014,3,21),date(2014,4,29),date(2014,5,3),date(2014,5,4),date(2014,5,5),\
                             date(2014,7,21),date(2014,9,15),date(2014,9,23),date(2014,10,13),date(2014,11,3),date(2014,11,24),date(2014,12,23))
        self.holiday_2015 = (date(2015,1,1),date(2015,1,12),date(2015,2,11),date(2015,3,21),date(2015,4,29),date(2015,5,3),date(2015,5,4),date(2015,5,5),\
                             date(2015,7,20),date(2015,9,21),date(2015,9,23),date(2015,10,12),date(2015,11,3),date(2015,11,23),date(2015,12,23))
        self.holiday_2016 = (date(2016,1,1),date(2016,1,11),date(2016,2,11),date(2016,3,21),date(2016,4,29),date(2016,5,3),date(2016,5,4),date(2016,5,5),\
                             date(2016,7,18),date(2016,9,19),date(2016,9,22),date(2016,10,10),date(2016,11,3),date(2016,11,23),date(2016,12,23))
        self.holidays = {2014:self.holiday_2014, 2015:self.holiday_2015, 2016:self.holiday_2016}
        self.dst_2015 = (datetime(2015, 3, 29, 1, 0, 0), datetime(2015, 10, 25, 2, 0, 0))
        self.dst_2016 = (datetime(2016, 3, 27, 1, 0, 0), datetime(2016, 10, 30, 2, 0, 0))
        self.dst = {2015:self.dst_2015, 2016:self.dst_2016}
        print(self.this_now)

    def set_tzconv(self, flag):
        self.tzconv=flag
        print('Timezone conversion: ', flag)
        
    def set_biz_start_time(self, start_hour):
        self.biz_start_time = start_hour
        print('Business hour start at ', start_hour)

    def get_jst(self, ddd):
        if self.tzone_conv:
            if self.tzone == TZONE_UTC:
                jst = ddd + timedelta(hours=9)
            else: 
                if ddd > self.dst[ddd.year][0] and ddd < self.dst[ddd.year][1]:
                    jst = ddd + timedelta(hours=8)
                else:
                    jst = ddd + timedelta(hours=9)
        else:
            jst = ddd + timedelta(hours=9)
        return jst
        
    def is_holiday(self, ddd):
        #print('IN: is_holiday(', ddd.date(), ')')
        if ddd.date() in self.holidays[ddd.year]:
            return True
        else:
            return self.is_weekend(ddd)

    def is_weekend(self, ddd):
        #print('IN: is_weekend(', ddd.date(), ')')
        if ddd.weekday() > 4:
            return True
        else:
            return False

    def get_next_bizday(self, ddd):
        #print('IN: get_next_bizday(', ddd.date(), ')')
        bizday = ddd + timedelta(days=1)
        while self.is_holiday(bizday):
            print('HOLIDAY')
            bizday = bizday + timedelta(days=1)
        return bizday

    def get_prev_bizday(self, ddd):
        #print('IN: get_prev_bizday(', ddd.date(), ')')
        bizday = ddd - timedelta(days=1)
        while self.is_holiday(bizday):
            print('HOLIDAY')
            bizday = bizday - timedelta(days=1)
        return bizday
        
    def get_adjusted_start(self, ddd):
        print('IN: get_adjusted_start(', ddd, ')')
        if self.is_holiday(ddd) or ddd.hour > 17:
            bizday = datetime.combine(self.get_next_bizday(ddd).date(), time(self.biz_start_time, 0, 0))
        elif ddd.hour < self.biz_start_time:
            bizday = datetime.combine(ddd.date(), time(self.biz_start_time, 0, 0))
        else:
            bizday = ddd
        return bizday
    
    def get_adjusted_end(self, ddd):
        print('IN: get_adjusted_end(', ddd, ')')
        if self.is_holiday(ddd) or ddd.hour < self.biz_start_time:
            bizday = datetime.combine(self.get_prev_bizday(ddd).date(), time(18, 0, 0))
        elif ddd.hour > 17:
            bizday = datetime.combine(ddd.date(), time(18, 0, 0))
        else:
            bizday = ddd
        return bizday

    def get_business_elapse(self, ddstart, ddend):
        print('IN: get_business_elapse(', ddstart, ',', ddend, ')')
        jststart = self.get_jst(ddstart)
        jstend = self.get_jst(ddend)
        print('jststart=', jststart, ', jstend=', jstend)
        adjstart = self.get_adjusted_start(jststart)
        adjend = self.get_adjusted_end(jstend)
        print('adjstart=', adjstart, ', adjend=', adjend)
        delta = adjend - adjstart
        elapseday = adjend.date() - adjstart.date()
        print('elapse days: ', elapseday.days)
        if elapseday.days > 0:
            curday = adjstart
            while adjend.date() > curday.date():
                if self.is_holiday(curday):
                    delta = delta - timedelta(hours=24)
                elif self.biz_start_time==9:
                    delta = delta - timedelta(hours=15)
                else:
                    delta = delta - timedelta(hours=14)
                curday = curday + timedelta(days=1)
        
        return delta.total_seconds()/60
        

