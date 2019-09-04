from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

####### BASIC SQLALCHEMY OBJECT-RELATIONAL-MAPPINGS #######
Base = declarative_base()
class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", back_populates="channels")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    users = relationship("User", back_populates="addresses")


if __name__ == '__main__':
    engine = create_engine('mysql://tshatti:tshattipassu@localhost:3306')
    Base.metadata.create_all(engine)