from datetime import datetime, timedelta, date
from collections import namedtuple
from .config import config
from .models import Notification

NotificationCategory = namedtuple("NotificationCategory", ["name", "label", "icon_path", "handler"])
def register(name, label, icon_path, handler):
    """
    Examples:
    register('wordy.new_game', 'New game', 'new_game.png', wordy_game_forward)
    register('wordy.new_move', 'New move', 'new_move.png', wordy_game_forward)
    register('wordy.game_lost', 'Game lost', 'game_lost.png', wordy_view_stats)
    """
    
    if name in config['handlers']:
        raise KeyError("{} already exists".format(name))
    
    nc = NotificationCategory(name, label, icon_path, handler)
    config['handlers'][name] = nc

def send(user, category, message, data, expires=None):
    """
    Category is the key for the registered notification type
    Message is the message that will be displayed in the rectangle
    Data is a string containing information passed to the handler function (as a string)
    Expires is either the datetime it expires or a timedelta of how long it will last
    
    Examples:
    send(1, "wordy.new_move", "Fred has made a move", "15", timedelta(hours=6))
    send(1, "wordy.new_game", "Bob has started a game with you", "20", timedelta(hours=6))
    send(1, "wordy.game_lost", "Gemma has won the game", "12", timedelta(hours=6))
    """
    
    # If it's a timedelta then convert it to a datetime
    if isinstance(expires, timedelta):
        expires = datetime.now() + expires
    
    # If it's a date then make it a datetime to enusre it'll go into the database fine
    if isinstance(expires, date):
        expires = datetime(expires.year, expires.month, expires.day)
    
    n = Notification(
        user     = user,
        message  = message,
        category = category,
        data     = data,
        expires  = expires,
        posted   = datetime.now(),
    )
    
    config['DBSession'].add(n)
