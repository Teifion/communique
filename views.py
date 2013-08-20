import transaction
import datetime

from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer

from .config import config
from . import lib

def home(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    return dict(
        title        = "Communique",
        layout       = layout,
        the_user     = the_user,
        notifications = lib.get_notifications(user_id=the_user.id),
    )

def save_preferences(request):
    the_user = config['get_user_func'](request)
    
    # Do stuff here
    if "form.submitted" in request.params:
        pass
    
    return HTTPFound(location=request.route_url('communique.home'))

def view(request):
    notification_id = request.matchdict['notification_id']
    
