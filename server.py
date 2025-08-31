from fastapi import FastAPI
from sqlalchemy import or_
from sqlalchemy import select

import crud
from lifespan import lifespan
from models import Adv
from crud import get_adv_by_id, add_adv, delete_adv
from dependency import SessionDependency
from schema import (CreateAdvResponse,CreateAdvRequest,SearchAdvResponse,
DeleteAdvResponse,UpdateAdvResponse,GetAdvResponse,UpdateAdvRequest)


app = FastAPI(title="Adv API",
              description="purchase/sale ad service",
              lifespan=lifespan
              )

@app.post("/adv/v1/",tags = ["advertisement"], response_model=CreateAdvResponse)
async def create_adv(adv:CreateAdvRequest,session:SessionDependency):
    adv_dict = adv.model_dump(exclude_unset=True)
    adv_orm_obj = Adv(**adv_dict)
    await add_adv(session,adv_orm_obj)
    return adv_orm_obj.id_dict


@app.get("/adv/v1/{adv_id}",tags = ["advertisement"], response_model=GetAdvResponse)
async def get_adv(adv_id:int,session:SessionDependency):
    adv_orm_obj = await get_adv_by_id(session, adv_id, orm_cls=Adv)
    return adv_orm_obj.to_dict


@app.get("/adv/search/",tags = ["advertisement"], response_model=SearchAdvResponse)
async def search_adv(session:SessionDependency, header:str):
    query = (select(Adv)
             .where((Adv.header == header))
             .limit(1000))
    list_adv = await session.scalars(query)
    return {"result":[adv.to_dict for adv in list_adv]}




@app.patch("/adv/v1/{adv_id}",tags = ["advertisement"], response_model=UpdateAdvResponse)
async def update_adv(adv_id:int, adv_data:UpdateAdvRequest,session:SessionDependency):
    adv_dict = adv_data.model_dump(exclude_unset=True)
    adv_orm_obj = await get_adv_by_id(session, adv_id, orm_cls=Adv)
    for field, value in adv_dict.items():
        setattr(adv_orm_obj,field,value)
    await add_adv(session,adv_orm_obj)
    return {"status":"success"}


@app.delete("/adv/v1/{adv_id}",tags = ["advertisement"], response_model=DeleteAdvResponse)
async def delete_adv(adv_id:int,session:SessionDependency):
    adv_orm_obj = await get_adv_by_id(session, adv_id, orm_cls=Adv)
    await  crud.delete_adv(session, adv_orm_obj)
    return {"status":"success"}