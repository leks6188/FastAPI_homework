from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import Adv
from sqlalchemy.ext.asyncio import AsyncSession


async def add_adv(session:AsyncSession,adv:Adv):
    session.add(adv)
    try:
        await session.commit()

    except IntegrityError as err:
        raise HTTPException(409,"Advertisement already exist")

async def get_adv_by_id(session:AsyncSession, adv_id:int, orm_cls):
    orm_obj = await session.get(orm_cls,adv_id)
    if orm_obj is None:
        raise  HTTPException(404, "Advertisement not found")

    return orm_obj


async def delete_adv(session:AsyncSession, adv_obj):
    await session.delete(adv_obj)
    await session.commit()
