from fastapi import FastAPI, Path
from typing import Annotated, Set

app = FastAPI()

@app.get("/user/{user_id}")
async def user_page(user_id:int = Path(ge=1, le=100, description="Enter User ID", example="25")) -> str:
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/user/{username}/{age}")
async def data_page(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                  example="UrbanUser")], age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    return f'Информация о пользователе. Имя: {username},  Возраст: {age}'