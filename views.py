import transaction
import datetime

from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer

from .config import config
from . import lib

def home(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    # from . import api
    # api.send(1, "wordy.new_move", "Fred has made a move", "15")
    
    return dict(
        title        = "Communique",
        layout       = layout,
        the_user     = the_user,
        notifications = lib.get_current(user_id=the_user.id),
    )

def save_preferences(request):
    the_user = config['get_user_func'](request)
    
    # Do stuff here
    if "form.submitted" in request.params:
        pass
    
    return HTTPFound(location=request.route_url('communique.home'))

def view(request):
    notification_id = int(request.matchdict['notification_id'])
    the_notification = lib.get(notification_id)
    
    if the_notification is None:
        raise Exception("No notification found")
    
    handler = config['handlers'][the_notification.category].handler
    return handler(request, the_notification.data)
