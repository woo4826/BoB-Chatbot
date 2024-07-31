from sqlalchemy import Column, String, Integer, DateTime
from database import Base

class Access_Table(Base):
    __tablename__ = 'access_table'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    access_id = Column(String)
    access_time = Column(DateTime)
    channel_id = Column(String)
    
    def to_dict(self):
        return {
            "id": self.id,
            "access_id": self.access_id,
            "user_id": self.user_id,
            "channel_id": self.channel_id,
            "access_time": self.access_time.strftime("%Y-%m-%d %H:%M:%S") if self.access_time else None
        }
    
class User_Table(Base):
    __tablename__ = 'user_table'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)