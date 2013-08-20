from datetime import datetime
from collections import namedtuple
from .config import config
from .models import Notification

NotificationCategory = namedtuple("NotificationCategory", ["name", "label", "icon_path", "handler"])
def register(name, label, icon_path, handler):
    if name in config['handlers']:
        raise KeyError("{} already exists".format(name))
    
    nc = NotificationCategory(name, label, icon_path, handler)
    config['handlers']['name'] = nc

def send(user, message, category, data, expires=None):
    n = Notification(
        user = user,
        message = message,
        category = category,
        data = data,
        expires = expires,
        posted = datetime.now(),
    )
    
    config['DBSession'].add(n)
