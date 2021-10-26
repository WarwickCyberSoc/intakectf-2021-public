from fastapi import FastAPI,Request,Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
#could also use uuid4
from uuid import uuid1
import base64
import pickle
#import stuff people might use for command execution
import os
import subprocess
import requests



def errorPage(request,exceptionObj):
    return templates.TemplateResponse("error.html",{"request":request},status_code=500)
exceptions={
    500: errorPage,
    501: errorPage,
    404: errorPage,
    503: errorPage
}

class PickleUUID(object):
    def __init__(self):
        self.userUUID = str(uuid1())
    def __str__(self):
        return self.userUUID
    def __repr__(self):
        return self.userUUID

app = FastAPI(docs_url=None,redoc_url=None,exception_handlers=exceptions)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request:Request):
    response = RedirectResponse("/18d3bfa9-0f3b-4532-a7da-b6d2a95e5f49")
    return response

def cookieManager(request:Request):
    cookieID = request.cookies.get('uuid')
    if not cookieID:
        newUUID = PickleUUID()
        username = str(newUUID)
        cookieID = base64.b64encode(pickle.dumps(newUUID)).decode()
    else:
        username = pickle.loads(base64.b64decode(cookieID))
    return (cookieID,username)


def returnPage(request:Request,page:str):
    cookieID, username = cookieManager(request)
    response =  templates.TemplateResponse(page,{"request":request,"username":username})
    response.set_cookie("uuid",cookieID)
    return response

@app.get("/18d3bfa9-0f3b-4532-a7da-b6d2a95e5f49")
def firstChat(request:Request):
    return returnPage(request,"18d3bfa9-0f3b-4532-a7da-b6d2a95e5f49.html")


@app.get("/0d3ff84f-acc6-44b8-8460-cd60cc2cec78")
def secondChat(request:Request):
    return returnPage(request,"0d3ff84f-acc6-44b8-8460-cd60cc2cec78.html")


@app.get("/fc9d9182-ce69-4856-8f29-8dc799f98309")
def thirdChat(request:Request):
    return returnPage(request,"fc9d9182-ce69-4856-8f29-8dc799f98309.html")

@app.get("/27c62c21-eba9-492c-aeb1-fc790083de95")
def fourthChat(request:Request):
    return returnPage(request,"27c62c21-eba9-492c-aeb1-fc790083de95.html")