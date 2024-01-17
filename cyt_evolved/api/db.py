from sqlalchemy import create_engine,Column, Integer, String, JSON, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///../chasing_your_tail_evolved/cyt.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

class TimePresence(Base):
    __tablename__ = 'time_presence'
    id = Column(Integer, primary_key=True)
    mac_address = Column(String)
    first_time_since_cyt_launched = Column(Integer)
    last_time_since_cyt_launched = Column(Integer)
    zero_to_five = Column(Boolean)
    five_to_ten = Column(Boolean)
    ten_to_fifteen = Column(Boolean)
    fifteen_to_twenty = Column(Boolean)
    twenty_and_more = Column(Boolean)

class Whitelist(Base):
    __tablename__ = 'whitelist'
    id = Column(Integer,  primary_key=True)
    mac_address = Column(String)

    

class Devices(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    mac_address = Column(String)
    device_key = Column(String)
    type_of_connection = Column(String)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:    
        yield db
    finally:
        db.close()  

