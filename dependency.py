import datetime
from typing import Annotated
from fastapi import Depends,Header,HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from models import Session
import uuid
from models import Token
from sqlalchemy import select

TOKEN_TTL_SEC = 3600 * 48


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session

SessionDependency = Annotated[AsyncSession,Depends(get_session,use_cache=True)]

async def get_token(x_token:Annotated[uuid.UUID, Header()],session:SessionDependency)-> Token:
    query=select(Token).where(Token.token==x_token, Token.creation_time>=
                              (datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SEC)))
    token = await  session.scalar(query)
    if token is None:
        raise HTTPException(401, "Token not Found")
    return token

TokenDependency = Annotated[Token,Depends(get_token)]