from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String
from config import settings 
import asyncio
from typing import Annotated

sync_engine = create_engine(
    url= settings.DATABASE_URL_psycopg,
    echo= True,
    pool_size=5,
    max_overflow=10    
)

async_engine = create_async_engine(
    url= settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10    
)


session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

str_200 = Annotated[str,200]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_200: String(200)
    }

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self,col)}")
        return f"<{self.__class__.__name__} {','.join(cols)}>"