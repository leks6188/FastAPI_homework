from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncAttrs
from sqlalchemy.orm import DeclarativeBase,MappedColumn,mapped_column
from sqlalchemy import Integer, String, func, DateTime, Float
load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")



DSN = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
       f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")


engine = create_async_engine(DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase,AsyncAttrs):
    @property
    def id_dict(self):
        return {"id":self.id}


class Adv(Base):
    __tablename__ = "advertisement"
    id:MappedColumn[int]=mapped_column(Integer, primary_key=True)
    header:MappedColumn[str]=mapped_column(String,index=True)
    description:MappedColumn[str]=mapped_column(String)
    price:MappedColumn[float]=mapped_column(Float)
    owner:MappedColumn[str]=mapped_column(String,index=True)
    date_of_creation:MappedColumn[datetime]=mapped_column(DateTime,server_default=func.now())

    @property
    def to_dict(self):
        return {"id":self.id, "header":self.header,
                "description":self.description,
                "owner":self.owner, "price":self.price,
                "date_of_creation":self.date_of_creation.isoformat()}


async def init_orm():
    async  with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()