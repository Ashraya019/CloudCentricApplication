# this is where your database schema becomes code, this file is responsible for:
# defining database tables 
# defining columns and constraints 
# mapping python objects to SQL rows 
# supporting indexing and performance

# design decision:
# for our first entity (Item):
# integer primary key
# unique name 
# optional description 
# indexed feilds (important for performance) 
# clean naming

from sqlalchemy import Column, Integer, String
from app.db import Base

class Item(Base):
    # explicit table name
    __tablename__ = "items"

    # primary key, indexed for fast lookups, used by APIs and foreign keys later
    id = Column(Integer, primary_key=True, index=True)
    # required feild, unique constraint -> no deplicates, indexed -> fast queries
    name = Column(String(100), unique=True, nullable=False, index=True)
    # optional text feild, safe max length
    description = Column(String(225), nullable=True)

