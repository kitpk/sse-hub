import datetime
from enum import Enum 

class Datetime_Format(Enum):
    datetime_full   = 1 ,
    datetime_short  = 2 ,
    date_full       = 3 ,
    date_short      = 4 ,
    time_24         = 5 ,
    time_12         = 6 ,
    h_m_24          = 7 ,
    h_m_12          = 8 ,
    folder          = 9 ,
    name            = 10,
    datetime_full_mil = 11 ,


class Datetime : 
    
    def __init__(self,
        parent=None,
        time_zone="UTC",
        **data
    ): 
        super().__init__()
        self.parent = parent 
        self.time_zone = time_zone 
        self.data = data

    @staticmethod
    def get_now() : 
        return datetime.datetime.utcnow()
    
    @staticmethod 
    def datetime2str(
        param:datetime.datetime=datetime.datetime.utcnow(),
        formats:Datetime_Format=Datetime_Format.date_full,
        debug=None
    ):
        try :
            if formats is Datetime_Format.datetime_full :
                out = "%Y-%m-%d %H:%M:%S"
            elif formats is Datetime_Format.datetime_short :
                out = "%Y-%m-%d"
            elif formats is Datetime_Format.date_full :
                out = "%d %B %Y"
            elif formats is Datetime_Format.date_short :
                out = "%d %b %Y"
            elif formats is Datetime_Format.time_24 :
                out = "%H:%M:%S"
            elif formats is Datetime_Format.time_12 :
                out = "%I:%M:%S %p"
            elif formats is Datetime_Format.h_m_24 :
                out = "%H:%M"
            elif formats is Datetime_Format.h_m_12 :
                out = "%I:%M %p"
            elif formats is Datetime_Format.folder :
                out = "%Y-%m-%d"
            elif formats is Datetime_Format.name :
                out = "%Y-%m-%d_%H:%M:%S"
            elif formats is Datetime_Format.datetime_full_mil :
                out = "%Y-%m-%d %H:%M:%S.%f"

            return True,param.strftime(out)

        except Exception as e :

            if debug : 
                return False,"func \"datetime2str\" \n\terror :  {0}".format(e)
            return False,None

    @staticmethod 
    def str2datetime(
        param:str,
        formats:Datetime_Format=Datetime_Format.datetime_full_mil,
        debug=None
    ):
        try :
            if formats is Datetime_Format.datetime_full :
                out = "%Y-%m-%d %H:%M:%S"
            elif formats is Datetime_Format.datetime_short :
                out = "%Y-%m-%d"
            elif formats is Datetime_Format.date_full :
                out = "%d %B %Y"
            elif formats is Datetime_Format.date_short :
                out = "%d %b %Y"
            elif formats is Datetime_Format.time_24 :
                out = "%H:%M:%S"
            elif formats is Datetime_Format.time_12 :
                out = "%I:%M:%S %p"
            elif formats is Datetime_Format.h_m_24 :
                out = "%H:%M"
            elif formats is Datetime_Format.h_m_12 :
                out = "%I:%M %p"
            elif formats is Datetime_Format.folder :
                out = "%Y-%m-%d"
            elif formats is Datetime_Format.name :
                out = "%Y-%m-%d_%H:%M:%S"
            elif formats is Datetime_Format.datetime_full_mil :
                out = "%Y-%m-%d %H:%M:%S.%f"

            return True,datetime.datetime.strptime(param, out)

        except Exception as e :

            if debug : 
                return False,"func \"str2datetime\" \n\terror :  {0}".format(e)
            return False,None

    @staticmethod 
    def datetime_increase(param:datetime.datetime=datetime.datetime.utcnow(),day=0,hour=0,minute=0,sec=0):
        try :
            return (param + datetime.timedelta(days=day,hours=hour,minutes=minute,seconds=sec))
        except Exception as e :
            return None

    @staticmethod
    def datetime_decrease(param:datetime=datetime.datetime.utcnow(),day=0,hour=0,minute=0,sec=0):
        try :
            return (param - datetime.timedelta(days=day,hours=hour,minutes=minute,seconds=sec))
        except Exception as e :
            return None

    @staticmethod
    def datetime_compare(param,param2,_type="less"):
        try :
            param = param.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            param2 = param2.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            if _type : 
                return param < param2
            else :
                return param > param2
        except Exception as e :
            return None
  