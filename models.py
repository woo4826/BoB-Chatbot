from sqlalchemy import Column, String, Integer, DateTime
from database import Base

class Access_Table(Base):
    __tablename__ = 'access_table'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    access_id = Column(String)
    access_time = Column(DateTime)
    channel_id = Column(String)
    