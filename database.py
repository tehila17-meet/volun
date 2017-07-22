from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
Base = declarative_base()


class Volunteers(Base):
    __tablename__ = "volunteers"
    id = Column(Integer,primary_key=True)
    VolunteeringHours = relationship("VolunteeringHours")
    requests=relationship("Requests")
    newhourrequests = relationship("Request_Hour")
    feedback = relationship("Feedback")
    name = Column(String(255))
    password = Column(String(255))
    birthday = Column(String(255))
    email = Column(String(255))
    gender = Column(String(255))
    profile = Column(String(255))
    interests = Column(String(255))
    phonenumber = Column(String(10))
    city = Column(String(255))
    pastorganizations = Column(String(255))
    goal_hour = Column(Integer)
    about = Column(String(255))




class Organizations(Base):
    __tablename__="organizations"
    id=Column(Integer,primary_key=True)
    volunteeringhours = relationship("VolunteeringHours")
    requests=relationship("Requests")
    newhourrequests = relationship("Request_Hour")
    feedback = relationship("Feedback")
    name = Column(String(255))
    password = Column(String(255))
    creationdate = Column(String(255))
    email = Column(String(255))
    description = Column(String)
    shortdescription = Column(String(50))
    profile = Column(String(255))
    background = Column(String(255))
    fields = Column(String(255))
    city = Column(String(255))

class VolunteeringHours(Base):
    __tablename__="volunteeringhours"
    id=Column(Integer,primary_key=True)
    volunteer_id= Column(Integer, ForeignKey('volunteers.id'))
    hours =Column(Integer)
    organization_id= Column(Integer,ForeignKey('organizations.id'))

class Requests(Base):
    __tablename__ = 'request'
    id = Column(Integer,primary_key = True)
    organization_id = Column(Integer,ForeignKey('organizations.id'))
    start_time = Column(String)
    volunteer_id = Column(Integer,ForeignKey("volunteers.id"))
    accepted = Column(Integer)#1is accepted 0 is still not answered 2 is rejected
    worked = Column(Integer)#1 is finished 0is yet no finished 2is rejected
    length = Column(Integer)
    date = Column(String(255))

class Request_Hour(Base):
    __tablename__ = 'requesthour'
    id = Column(Integer, primary_key = True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    volunteer_id = Column(Integer,ForeignKey("volunteers.id"))
    worked = Column(Integer)




class Feedback(Base):
    __tablename__ = 'feedback'
    id  = Column(Integer, primary_key = True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    feedback = Column(String(255))
    volunteer_id = Column(Integer, ForeignKey('volunteers.id'))



engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()
