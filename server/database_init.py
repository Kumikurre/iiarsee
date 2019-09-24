import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship

####### BASIC SQLALCHEMY OBJECT-RELATIONAL-MAPPINGS #######
Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('channel_id', Integer, ForeignKey('channels.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="users")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    nickname = Column(String(32), nullable=False)
    address = relationship("addresses")
    channels = relationship(
        "Channel",
        secondary=association_table,
        back_populates="users")


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    ip4_address = Column(String(64), nullable=False)
    ip6_address = Column(String(64))


def initialize(engine, logger):
    try:
        engine.execute("CREATE DATABASE iiarsee") #create db
    except Exception:
        logger.info('Database most likely exists')
    engine.execute("USE iiarsee") # select new db
    logger.info('Creating tables...')
    try:
        Base.metadata.create_all(engine)
    except Exception:
        logger.info('Fug, something went wrong :(')
    else:
        logger.info('Tables created')
    

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    engine = create_engine('mysql://tshatti:tshattipassu@db:3306')
    
    initialize(engine, logger)