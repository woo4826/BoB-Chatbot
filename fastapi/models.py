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
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }

class IocLog_Table(Base):
    __tablename__ = 'ioc_log_table'
    
    id = Column(Integer, primary_key=True, index=True)
    access_user_id = Column(String)
    access_ch_id = Column(String)
    message_text = Column(String)
    access_time = Column(DateTime)
    
    def to_dict(self):
        return {
            "id": self.id,
            "access_user_id": self.access_user_id,
            "access_ch_id": self.access_ch_id,
            "message_text": self.message_text,
            "access_time": self.access_time.strftime("%Y-%m-%d %H:%M:%S") if self.access_time else None
        }