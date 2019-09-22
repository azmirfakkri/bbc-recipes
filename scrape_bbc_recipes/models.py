from datetime import datetime
from sqlalchemy import create_engine, Column
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

# TODO: need to create many-to-many relationship


class Recipe(DeclarativeBase):
    """
    Recipe model
    """
    __tablename__ = 'recipes'
    __table_args__ = {'schema': 'recipes'}

    recipe_id_nk = Column('recipe_id_nk', BigInteger, primary_key=True)
    title = Column('title', String, nullable=True)
    recipe_description = Column('recipe_description', String, nullable=True)
    recipe_url = Column('recipe_url', String, nullable=True)
    recipe_type = Column('recipe_type', String, nullable=True)
    prep_time = Column('prep_time', String, nullable=True)
    cooking_time = Column('cooking_time', String, nullable=True)
    serves = Column('serves', String, nullable=True)
    dietary = Column('dietary', String, nullable=True)
    methods = Column('methods', String, nullable=True)
    ingredients = Column('ingredients', String, nullable=True)
    inserted_at = Column('inserted_at', DateTime, default=datetime.now)


class RawIngredient(DeclarativeBase):
    """
    Recipe model
    """
    __tablename__ = 'raw_ingredients'
    __table_args__ = {'schema': 'recipes'}

    raw_id = Column('raw_id', Integer, primary_key=True, autoincrement=True)
    raw_ingredient = Column('ingredient', String, nullable=True)
    inserted_at = Column('inserted_at', DateTime, default=datetime.now)
