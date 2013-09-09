from sqlalchemy import or_, func
from .config import config
from datetime import datetime, timedelta

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
    
    return config['DBSession'].query(Notification).filter(*filters).order_by(Notification.read.asc(), Notification.posted.desc()).limit(20)

def get_current_count(user_id):
    now = datetime.now()
    
    filters = (
        Notification.user == int(user_id),
        Notification.posted < now,
        Notification.read == False,
        or_(Notification.expires > now, Notification.expires == None),
    )
    
    return config['DBSession'].query(func.count(Notification.id)).filter(*filters).first()[0]

def delete(the_notification):
    config['DBSession'].delete(the_notification)

def mark_as_read(the_notification):
    max_expires = datetime.now() + timedelta(hours=12)
    
    if the_notification.expires == None:
        the_notification.expires = max_expires
    
    the_notification.expires = min(max_expires, the_notification.expires)
    the_notification.read = True
    
    config['DBSession'].add(the_notification)

def clear(user_id, clear_all=False):
    filters = [Notification.user == user_id]
    
    if not clear_all:
        filters.append(Notification.read == True)
    
    config['DBSession'].query(Notification).filter(*filters).delete()

def count_of_category(user_id, category):
    return config['DBSession'].query(func.count(Notification.id)).filter(
        Notification.user == user_id,
        Notification.category == category,
    ).first()[0]

def cleanup():
    """
    Deletes all expired notifications
    """
    
    config['DBSession'].query(Notification).filter(
        Notification.expires < datetime.now(),
    ).delete()

def get_user(username):
    # My usernames are all uppercase so I'm applying this, not sure how to make this more generic yet sorry
    username = username.strip().upper()
    r = config['DBSession'].query(config['User'].id).filter(config['User'].name == username).first()
    
    if r is None:
        return None
    return r[0]
