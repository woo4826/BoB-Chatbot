from typing import Optional
from pydantic import BaseModel # pylint: disable=no-name-in-module
from datetime import datetime

class Access_Data(BaseModel):
    user_id: Optional[str] = None
    channel_id : Optional[str] = None
    access_time : Optional[datetime] = None
    access_id : Optional[str] = None
    
    class Config :
        orm_mode = True
        
        
class User_Data(BaseModel):
    user_id: Optional[str] = None
    
    class Config :
        orm_mode = True
        
        
#
# access_user_id
# access_ch_id
# message_text
# access_time
class IoC_Log(BaseModel):
    access_user_id: Optional[str] = None
    access_ch_id : Optional[str] = None
    message_text : Optional[str] = None
    access_time : Optional[datetime] = None
    
    class Config :
        orm_mode = True
class IoC_Data(BaseModel):
    ioc_item: Optional[str] = None
    ioc_type: Optional[str] = None
    
    class Config :
        orm_mode = True