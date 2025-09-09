from fastapi import FastAPI, HTTPException
from sqlalchemy import select
import crud
from auth import check_password, hash_password
from lifespan import lifespan
from models import Adv,User,Token
from crud import get_item_by_id, add_item, delete_item
from dependency import SessionDependency,TokenDependency
from schema import (CreateAdvResponse, CreateAdvRequest, SearchAdvResponse,
                    DeleteAdvResponse, UpdateAdvResponse, GetAdvResponse, UpdateAdvRequest,
                    CreateUserResponse, CreateUserRequest, LoginResponse,
                    UpdateUserRequest,LoginRequest,DeleteUserResponse)


app = FastAPI(title="Adv API",
              description="purchase/sale ad service",
              lifespan=lifespan
              )


@app.post("/adv/v1/user",tags=["users"],response_model=CreateUserResponse)
async def create_user(user_data:CreateUserRequest,session:SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_orm_obj = User(**user_dict)
    await crud.add_item(session,user_orm_obj)
    return user_orm_obj.dict


@app.get("/adv/v1/user/{user_id}", tags=["users"])
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await get_item_by_id(session, user_id, orm_cls=User)
    return user_orm_obj.dict


@app.patch("/adv/v1/user/{user_id}",tags = ["users"])
async def update_user(user_id:int, user_data:UpdateUserRequest,
                     session:SessionDependency,token:TokenDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_orm_obj = await get_item_by_id(session, user_id, orm_cls=User)
    if token.user.role == "admin" or user_orm_obj.id == token.user.id:
        for field, value in user_dict.items():
            setattr(user_orm_obj,field,value)
        await crud.add_item(session,user_orm_obj)
        return {"status":"success"}
    raise HTTPException(403, "Insufficient user rights")


@app.delete("/adv/v1/user/{user_id}",tags = ["users"],response_model=DeleteUserResponse)
async def delete_user(user_id:int,session:SessionDependency,token:TokenDependency):
    user_orm_obj = await get_item_by_id(session, user_id, orm_cls=User)
    if token.user.role == "admin" or user_orm_obj.id == token.user.id:
        await  crud.delete_item(session, user_orm_obj)
        return {"status":"success"}
    raise HTTPException(403, "Insufficient user rights")




@app.post("/adv/v1/login",tags=["login"],response_model=LoginResponse)
async def login(login_data:LoginRequest,session:SessionDependency):
    query = select(User).where(User.name == login_data.name)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(401, "Invalid credentials")
    if not check_password(login_data.password,user.password):
        raise HTTPException(401, "Invalid credentials")
    token = Token(user_id=user.id)
    await add_item(session,token)
    return token.dict




@app.post("/adv/v1/",tags = ["advertisement"], response_model=CreateAdvResponse)
async def create_adv(adv:CreateAdvRequest,session:SessionDependency,token:TokenDependency ):
    adv_dict = adv.model_dump(exclude_unset=True)
    adv_orm_obj = Adv(**adv_dict,user_id = token.user_id)
    await crud.add_item(session,adv_orm_obj)
    return adv_orm_obj.to_dict


@app.get("/adv/v1/{adv_id}",tags = ["advertisement"], response_model=GetAdvResponse)
async def get_adv(adv_id:int,session:SessionDependency):
    adv_orm_obj = await get_item_by_id(session, adv_id, orm_cls=Adv)
    return adv_orm_obj.to_dict


@app.get("/adv/search/",tags = ["advertisement"], response_model=SearchAdvResponse)
async def search_adv(header:str, session:SessionDependency):
    query = (select(Adv)
             .where((Adv.header == header))
             .limit(1000))
    result = await session.execute(query)
    adv_list = result.unique().scalars().all()
    return {"result": [adv.to_dict for adv in adv_list]}



@app.patch("/adv/v1/{adv_id}",tags = ["advertisement"], response_model=UpdateAdvResponse)
async def update_adv(adv_id:int, adv_data:UpdateAdvRequest,
                     session:SessionDependency,token:TokenDependency):
    adv_dict = adv_data.model_dump(exclude_unset=True)
    adv_orm_obj = await get_item_by_id(session, adv_id, orm_cls=Adv)
    if token.user.role == "admin" or adv_orm_obj.user_id == token.user.id:
        for field, value in adv_dict.items():
            setattr(adv_orm_obj,field,value)
        await crud.add_item(session,adv_orm_obj)
        return {"status":"success"}
    raise HTTPException(403, "Insufficient user rights")


@app.delete("/adv/v1/{adv_id}",tags = ["advertisement"], response_model=DeleteAdvResponse)
async def delete_adv(adv_id:int,session:SessionDependency,token:TokenDependency):
    adv_orm_obj = await get_item_by_id(session, adv_id, orm_cls=Adv)
    if token.user.role == "admin" or adv_orm_obj.user_id == token.user.id:
        await  delete_item(session, adv_orm_obj)
        return {"status":"success"}
    raise HTTPException(403, "Insufficient user rights")

