from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
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


if __name__ == '__main__':
    engine = create_engine('mysql://tshatti:tshattipassu@127.0.0.1:3306')
    try:
        engine.execute("CREATE DATABASE iiarsee") #create db
    except Exception:
        print('Database most likely exists')
    engine.execute("USE iiarsee") # select new db
    print('Creating tables...')
    try:
        Base.metadata.create_all(engine)
    except Exception:
        print('Fug, something went wrong :(')
    else:
        print('Tables created')
    