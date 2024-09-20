from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

from scrapper import getUser
from svg import svg
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get('/{username}')
async def userCard(username: str):
    """
    Endpoint to extract the user data and generate the svg image
    """
    data = getUser(username)
    if 404 == data:
        return "User Not Found"
    user_data = data[1]
    if user_data:
        dwg = svg(user_data)
        return Response(content = dwg.tostring(),media_type='image/svg+xml')
    return "Error Creating kaggle card"
