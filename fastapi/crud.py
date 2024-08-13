import datetime
import hashlib
from sqlalchemy.orm import Session

import models
from schema import Access_Data, IoC_Log

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

def get_ioc(db: Session):
    ioc_list = db.query(models.Access_Table).all()
    return [ioc.to_dict() for ioc in ioc_list]

def get_users(db: Session):
    user_list = db.query(models.User_Table).all()
    return [user.to_dict() for user in user_list]



def write_ioc_log(log:IoC_Log, db: Session):
    print(log)
    new_log = models.IocLog_Table(
        access_user_id=log.access_user_id,
        access_ch_id=log.access_ch_id,
        message_text=log.message_text,
        access_time=log.access_time or datetime.datetime.utcnow(),
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
     
        
def get_server_data():
    import os 
    import time
    import locale
    return {
        "host_info": {
            "system": os.uname().sysname,
            "node": os.uname().nodename,
            "release": os.uname().release,
            "version": os.uname().version,
            "machine": os.uname().machine,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "locale": locale.getdefaultlocale()
        },
        "system_status": {
            "disk": os.popen("df -h").read().strip()
        },

        "security": {
            # "firewall_rules": os.popen("sudo iptables -L").read().strip(),
            "recent_logins": os.popen("last -n 5").read().strip()
        },
    }
    