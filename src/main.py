from fastapi import FastAPI, Response
from scrapper import getUser
from svg import svg
app = FastAPI()

@app.get('/{username}')
async def userCard(username: str):
    data = getUser(username)
    if 404 == data:
        return "User Not Found"
    user_data = data[1]
    dwg = svg(user_data)
    return Response(content = dwg.tostring(),media_type='image/svg+xml')
