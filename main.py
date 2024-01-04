from fastapi import FastAPI
from pathlib import Path
import importlib
import os

from pydantic import BaseSettings

import logging

#current path
BASE_DIR = Path(__file__).resolve().parent
APP_DIR  = Path(BASE_DIR).joinpath("app")
SETTING_DIR  = Path(BASE_DIR).joinpath("config").joinpath("dev").joinpath("env.yaml")

from core.common.config import Setting
Settings = Setting()
Settings.__load__(file=SETTING_DIR,name="BASE")


#instance app
app = FastAPI(
    title="SSEHub",
    root_path="",
)

app.__setattr__("custom_setting",Settings)

model = []

#include redis_streaming or memory_streaming
for temp in list(os.walk(APP_DIR))[1:] :
    if app.custom_setting.data['BASE']['sse_hub']['redis']:
        if 'redis_streaming.py' in temp[1:][1]  :
            try :
                name = Path(temp[0]).name
                i = importlib.import_module('app.'+name+'.redis_streaming')
                i.app.__setattr__("custom_setting",Settings)
                app.mount(
                    path=i.prefix,
                    app=i.app,
                    name=f"app_{name}",
                )
            except Exception as e :
                logging.error("redis_streaming : {0} can't load \n\t{1}".format(name,e))
    else:
        if 'memory_streaming.py' in temp[1:][1]  :
            try :
                name = Path(temp[0]).name
                i = importlib.import_module('app.'+name+'.memory_streaming')
                i.app.__setattr__("custom_setting",Settings)
                app.mount(
                    path=i.prefix,
                    app=i.app,
                    name=f"app_{name}",
                )
            except Exception as e :
                logging.error("memory_streaming : {0} can't load \n\t{1}".format(name,e))
               
@app.on_event('startup')
async def startup():
    print("startup")
    url_list = [
        {"path": route.path, "name": route.name} for route in app.routes
    ]
    print(url_list)

@app.on_event('shutdown')
async def shutdown():
    print("shutdown")

model += [
    'aerich.models',
]

name = 'default'
