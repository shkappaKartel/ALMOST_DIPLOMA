from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/', response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name='users.html', context={'users': users})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_user(
    request: Request,
    user_id: Annotated[int, Path(ge=1, le=100,
                                 description='Enter User ID', example='1')]
):
    for u in users:
        if u.id == user_id:
            return templates.TemplateResponse(
                request=request, name='users.html', context={'user': u})
    raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}', response_model=User)
async def post_user(
    username: Annotated[str, Path(min_length=5, max_length=20,
                                  description='Enter username',
                                  example='UrbanUser')],
    age: Annotated[int, Path(ge=18, le=120, description='Enter age',
                             example=24)]
):
    user_id = max((u.id for u in users), default=0) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100,
                                 description='Enter User ID', example='1')],
    username: Annotated[str, Path(min_length=5, max_length=20,
                                  description='Enter username',
                                  example='UrbanUser')],
    age: Annotated[int, Path(ge=18, le=120, description='Enter age',
                             example=24)]
):
    for u in users:
        if u.id == user_id:
            u.username = username
            u.age = age
            return u
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}', response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(ge=1, le=100,
                                 description='Enter User ID', example='1')]
):
    for i, u in enumerate(users):
        if u.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail='User was not found')