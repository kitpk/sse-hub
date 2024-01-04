import yaml
import logging
import pathlib


class Setting : 
    def __init__(self,parent=None,debug=False) :
        super().__init__()
        self.parent = parent
        self.debug = debug
        self.data = {}

    def __load__(self,file=None,name=None):
        try : 
            temp_path = pathlib.Path(file)
            if not temp_path.exists() : 
                raise Exception("file config not found")
            if name is None : 
                name = temp_path.name
            with open(file,'r') as file : 
                self.data[name] = yaml.full_load(file)
            return True
        except Exception as e : 
            if self.debug : 
                logging.error("error __load_config__ >> {0}".format(e))
            return False
    
    def __write__(self,file=None,name=None) :
        try :
            if name is None :
                raise Exception("param 'name' must require")
            if name not in self.data.keys() : 
                self.data[name]  = {}
            temp_path = pathlib.Path(file)
            with open(file,'w+') as file : 
                doc = yaml.dump(self.data[name],file,default_flow_style=False)
            return True 
        except Exception as e :
            print(e)
            return False

