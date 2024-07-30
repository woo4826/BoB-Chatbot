import datetime
import hashlib
from sqlalchemy.orm import Session

from models import Access_Table
from schema import Access_Data



def write_access_data( access_item: Access_Data, db: Session):
    
    new_access = Access_Table(
        user_id=access_item.user_id,
        channel_id=access_item.channel_id,
        access_time=access_item.access_time or datetime.datetime.utcnow(),
    )
    new_access.access_id = hashlib.sha256((str(new_access.access_time) + access_item.channel_id + access_item.user_id).encode()).hexdigest()
    db.add(new_access)
    db.commit()
    db.refresh(new_access)
    # db.commit()
    return 
# """
# Make access id
# -- access_id = sha256(access_time + channel_id + user_id)
# Write access id to database
# Test data:
# {
# "user_id":"han",
# "channel_id":"hantest",
# "access_time":"2023-07-23T11:22:00.000000"
# }
# """ 