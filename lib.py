from sqlalchemy import or_, func
from .config import config
from datetime import datetime

from . models import Notification

def get(notification_id):
    return config['DBSession'].query(Notification).filter(Notification.id == int(notification_id)).first()

def get_current(user_id):
    now = datetime.now()
    
    filters = (
        Notification.user == int(user_id),
        Notification.posted < now,
        or_(Notification.expires > now, Notification.expires == None),
    )
    
    return config['DBSession'].query(Notification).filter(*filters).order_by(Notification.posted.desc())

def get_current_count(user_id):
    now = datetime.now()
    
    filters = (
        Notification.user == int(user_id),
        Notification.posted < now,
        or_(Notification.expires > now, Notification.expires == None),
    )
    
    return config['DBSession'].query(func.count(Notification.id)).filter(*filters).first()[0]

def delete(the_notification):
    config['DBSession'].delete(the_notification)

def clear(user_id):
    config['DBSession'].query(Notification).filter(Notification.user == user_id).delete()
