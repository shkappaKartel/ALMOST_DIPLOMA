from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, Возраст: 18'}

@app.get('users')
async def get_users() -> dict:
    return users

@app.post('/user/{username}/{age}')
async def post_user(username: Annotated[str, Path(max_length=30, description='Введите имя', example='Petr')],
                    age: Annotated[int, Path(le=120, description='Введите имя', example='Ivanov')]) -> str:
    new_user_id = str(int(max(users, key=int)) + 1)
    users[new_user_id] = f'Имя: {username}: Возраст: {age}'
    return f'Пользователь {new_user_id} зарегистрирован.'

@app.put('/user/{user_id}/{username}/{age}')
async def put_users(user_id: int, username: Annotated[str, Path(max_length=30, description='Введите своё имя', example='Ivan')],
                    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example='24')]) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'Пользователь {user_id} обновлён'

app.delete('/user/{user_id}')
async def del_users(user_id: Annotated[str, Path(description='Введите ID для удаления', example='1')]) -> str:
    users.pop(user_id)
    return f'Пользователь {user_id} удалён.'