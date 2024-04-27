from fastapi import APIRouter, Body
from models.models import Main_User, Main_UserDB, New_Respons
from typing import Annotated, Union

U_R = APIRouter()

def coder_passwd(cod: str):
    result = cod
    return result

users_list = [Main_UserDB(name = 'Имя', surname = 'Фамилия', id = 1, password = coder_passwd('12345678'))]

def find_user(id: int) -> Union[Main_UserDB, None]:
    for user in users_list:
        if user.id == id:
            return user
    return None

@U_R.get("/api/users", response_model = Union[list[Main_User], None])
async def get_users():
    return users_list

@U_R.put("/api/users", response_model = Union[Main_User, New_Respons])
async def edit_person(item: Annotated[Main_User, Body(embed = True, description = "Изменяем данные пользователя через его id")]):
    user = find_user(item.id)
    if user == None:
        return New_Respons(message = "Пользователь не найден")
    user.id = item.id
    user.name = item.name
    return user

@U_R.post("/api/users", response_model = Union[Main_User, New_Respons])
async def create_user(item: Annotated[Main_User, Body(embed = True, description = "Новый пользователь")]):
    user = Main_UserDB(name = item.name, surname = item.surname, id = item.id, password = coder_passwd(item.surname))
    users_list.append(user)
    return user

@U_R.get("/api/users/{id}", response_model = Union[Main_User, New_Respons])
async def get_user(id: int):
    user = find_user(id)
    print(user)
    if user == None:
        return New_Respons(message = "Пользователь не найден")
    return user

@U_R.delete("/api/users/{id}", response_model=Union[list[Main_User], None])
async def delete_person(id: int):
    user = find_user(id)
    if user == None:
        return New_Respons(message = "Пользователь не найден")
    users_list.remove(user)
    return users_list