import datetime
import hashlib
from sqlalchemy.orm import Session

import models
from schema import Access_Data

def user_exists( user_item: Access_Data, db: Session):
    user = db.query(models.User_Table).filter(models.User_Table.user_id == user_item.user_id).first()
    return user is not None 

def write_access_data( access_item: Access_Data, db: Session):
    new_access = models.Access_Table(
        user_id=access_item.user_id,
        channel_id=access_item.channel_id,
        access_time=access_item.access_time or datetime.datetime.utcnow(),
    )
    new_access.access_id = hashlib.sha256((str(new_access.access_time) + access_item.channel_id + access_item.user_id).encode()).hexdigest()
    db.add(new_access)
    db.commit()
    db.refresh(new_access)
    return 

def create_user( user_item: Access_Data, db: Session):
    # Check if user already exists
    check_user = db.query(models.User_Table).filter(models.User_Table.user_id == user_item.user_id).first()
    if check_user is not None:
        return False

    new_user = models.User_Table(
        user_id=user_item.user_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True