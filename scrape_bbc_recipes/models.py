import datetime
from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, BigInteger, String, DateTime)

from scrapy.utils.project import get_project_settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Recipes(DeclarativeBase):
    """
    Ads model
    """
    __tablename__ = 'recipes'

    recipe_id_nk = Column('recipe_id_nk', BigInteger, primary_key=True)
    title = Column('title', String)
    description = Column('description', String)
