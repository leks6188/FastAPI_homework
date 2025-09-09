from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models import ORM_CLS,ORM_OBJ

async def add_item(session:AsyncSession,item:ORM_OBJ):
    session.add(item)
    try:
        await session.commit()

    except IntegrityError as err:
        raise HTTPException(409,"Already exist")

async def get_item_by_id(session:AsyncSession, item_id:int, orm_cls):
    orm_obj = await session.get(orm_cls,item_id)
    if orm_obj is None:
        raise  HTTPException(404, "Not found")

    return orm_obj


async def delete_item(session:AsyncSession, item_obj):
    await session.delete(item_obj)
    await session.commit()
