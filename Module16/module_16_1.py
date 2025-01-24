from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get('/')
async def get_main_page() -> JSONResponse:
    return JSONResponse(content='Главная страница',
                        headers={'Content-Type': 'charset=utf-8'})


@app.get('/user/admin')
async def get_admin_page() -> JSONResponse:
    return JSONResponse(content='Вы вошли как администратор',
                        headers={'Content-Type': 'charset=utf-8'})


@app.get('/user/{user_id}')
async def get_user_id(user_id: int) -> JSONResponse:
    return JSONResponse(content=f'Вы вошли как пользователь № {user_id}',
                        headers={'Content-Type': 'charset=utf-8'})


@app.get('/user')
async def get_user_info(username: str = None, age: int = None) -> JSONResponse:
    if username is None and age is None:
        return JSONResponse(content='укажите параметры пользователя',
                            headers={'Content-Type': 'charset=utf-8'})
    if username is None:
        return JSONResponse(content='Не указан username',
                            headers={'Content-Type': 'charset=utf-8'})
    if age is None:
        return JSONResponse(content=f'Информация о пользователе. Имя: {username}, Возраст: не задан',
                            headers={'Content-Type': 'charset=utf-8'})
    else:
        return JSONResponse(content=f'Информация о пользователе. Имя: {username}, Возраст: {age}',
                            headers={'Content-Type': 'charset=utf-8'})