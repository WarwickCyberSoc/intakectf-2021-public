from fastapi import FastAPI,Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import subprocess
import re
def errorPage(request,exceptionObj):
    return templates.TemplateResponse("error.html",{"request":request},status_code=500)
exceptions={
    500: errorPage,
    404: errorPage,
    503: errorPage
}

app = FastAPI(docs_url=None,redoc_url=None,exception_handlers=exceptions)

templates = Jinja2Templates(directory="templates")
app.mount("/assets",StaticFiles(directory="assets"),name="assets")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",{"request":request,"runningCommand":""})

def formSubmitResponse(request:Request,response:str):
    # return content below submit box
    return templates.TemplateResponse("index.html",{"request":request,"runningCommand":response})



#submit page
@app.post("/")
def shell(request:Request,command:str=Form(...)):
    #could do more restrictions to doubly ensure it's the right command, but this is close enough

    ipAddress = request.client.host
    #could be /bin/sh /bin/bash /bin/zsh etc etc
    binInstring =re.findall(r"-e\s+/bin/\w*sh",command)
    if not binInstring or ipAddress not in command or "nc" not in command[:2]:
        #invalid command
        response="Invalid command"
    else:
        command+="&"
        subprocess.Popen(command,shell=True)
        response="Running your command..."
    return formSubmitResponse(request,response)