import uuid
from typing import Literal
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, func, DateTime, Float, UUID, ForeignKey

load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")

ROLE = Literal["user"]|Literal["admin"]

DSN = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
       f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")


engine = create_async_engine(DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)



class Base(DeclarativeBase,AsyncAttrs):
    @property
    def id_dict(self):
        return {"id":self.id}

class User(Base):
    __tablename__ = "user"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    name:MappedColumn[str]=mapped_column(String,unique=True)
    password:MappedColumn[str]=mapped_column(String)
    role:MappedColumn[ROLE]=mapped_column(String,default="user")

    tokens:MappedColumn[list["Token"]]=relationship("Token",
                                                    lazy="joined",back_populates="user",
                                                    cascade="all, delete-orphan",
                                                    passive_deletes=True)

    advertisements:MappedColumn[list["Adv"]]=relationship("Adv",
                                                    lazy="joined",back_populates="user",
                                                          cascade="all, delete-orphan",
                                                          passive_deletes=True)


    @property
    def dict(self):
        return {"id":self.id,
                "name":self.name}


class Token(Base):
    __tablename__ ="token"
    id:MappedColumn[int]=mapped_column(Integer, primary_key=True)
    token:MappedColumn[uuid.UUID]=mapped_column(UUID,unique=True,
                                                server_default=func.gen_random_uuid())

    creation_time:MappedColumn[datetime]=mapped_column(DateTime,server_default=func.now())
    user_id:MappedColumn[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"))
    user:MappedColumn["User"]=relationship("User",lazy="joined",back_populates="tokens")

    @property
    def dict(self):
        return {"token":self.token}

class Adv(Base):
    __tablename__ = "advertisement"
    id:MappedColumn[int]=mapped_column(Integer, primary_key=True)
    header:MappedColumn[str]=mapped_column(String,index=True)
    description:MappedColumn[str]=mapped_column(String)
    price:MappedColumn[float]=mapped_column(Float)
    owner:MappedColumn[str]=mapped_column(String,index=True)
    date_of_creation:MappedColumn[datetime]=mapped_column(DateTime,server_default=func.now())
    user_id:MappedColumn[int]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"))
    user: MappedColumn["User"] = relationship("User", lazy="joined",
                                              back_populates="advertisements")



    @property
    def to_dict(self):
        return {"id":self.id, "header":self.header,
                "description":self.description,
                "owner":self.owner, "price":self.price,
                "date_of_creation":self.date_of_creation.isoformat(),
                "user_id":self.user_id}



async def init_orm():
    async  with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()

ORM_OBJ = Adv|User|Token
ORM_CLS = type[Adv]|type[User]|type[Token]