from fastapi import FastAPI, HTTPException, Path
from typing import List, Annotated
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/user')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(
        username: Annotated[str, Path(min_length=3, max_length=30, description='Enter username', example='Kirill')]
        , age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=30)]) -> User:
    user_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=0, le=300, description='Enter user_id', example='1')]
        , username: Annotated[str, Path(min_length=3, max_length=30, description='Enter username', example='Kirill')]
        , age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=30)]) -> User:
    try:
        user = next((u for u in users if u.id == user_id))
        users[user_id-1] = User(id=user.id, username=username, age=age)
        return users[user_id]
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[int, Path(ge=0, le=300, description='Enter user_id', example='1')]) -> User:
    try:
        user = next((u for u in users if u.id == user_id))
        users.remove(user)
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")