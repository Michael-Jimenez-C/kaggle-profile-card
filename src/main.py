from typing import Optional
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from scrapper import getUser
from svg import svg
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")


templates = Jinja2Templates(directory="src/templates")

@app.get('/{username}')
async def userCard(username: str):
    """
    Endpoint to extract the user data and generate the svg image
    """
    data = getUser(username)
    if 404 == data:
        return "User Not Found"
    print(data)
    user_data = data[1]
    if user_data:
        dwg = svg(user_data)
        return Response(content = dwg.tostring(),media_type='image/svg+xml')
    return "Error Creating kaggle card"

@app.get('/', response_class=HTMLResponse)
async def demo(request: Request, username: Optional[str] = "username"):
    return templates.TemplateResponse(request=request, name="demo.html", context={"username": username})
