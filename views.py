import transaction
import datetime

from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer

from .config import config
from . import lib

def home(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    # Use this for testing
    # from . import api
    # api.send(1, "wordy.new_move", "Fred has made a move", "15")
    # api.send(1, "wordy.new_game", "Bob has started a game with you", "20")
    
    def notification_yield():
        for n in lib.get_current(user_id=the_user.id):
            handler = config['handlers'][n.category]
            yield n, handler
    
    return dict(
        title        = "Communique",
        layout       = layout,
        the_user     = the_user,
        notifications = notification_yield(),
    )

def action(request):
    the_user = config['get_user_func'](request)
    the_action = request.matchdict['action']
    
    if the_action == "clear":
        lib.clear(the_user.id)
    else:
        raise KeyError("No handler for action of '{}'".format(the_action))
    
    return HTTPFound(location=request.route_url('communique.home'))

def mini_home(request):
    request.do_not_log = True
    the_user = config['get_user_func'](request)
    
    output = []
    
    for n in lib.get_current(user_id=the_user.id):
        handler = config['handlers'][n.category]
        
        output.append("""
            <a class="communique-notification-row" href="{communique_view}">
                <img src="{icon}" class="communique-notification-icon" />
                <div class="communique-notification-text">
                    <strong>{title}</strong>: {message}
                </div>
            </a>
        """.format(
            icon = handler.icon_path,
            title = handler.label,
            message = n.message,
            communique_view = request.route_url('communique.view', notification_id=n.id),
        ))
    
    return "".join(output)

def home_count(request):
    request.do_not_log = True
    user_id = int(request.matchdict['user_id'])
    count = lib.get_current_count(user_id=user_id)
    
    # the_user = config['get_user_func'](request)
    # count = lib.get_current_count(user_id=the_user.id)
    return str(count)

def view(request):
    request.do_not_log = True
    the_user = config['get_user_func'](request)
    
    notification_id = int(request.matchdict['notification_id'])
    the_notification = lib.get(notification_id)
    
    if the_notification is None:
        layout = get_renderer(config['layout']).implementation()
        
        return dict(
            title   = "View notification",
            layout  = layout,
            message = "We couldn't find that notification!",
        )
    
    if the_notification.user != the_user.id:
        layout = get_renderer(config['layout']).implementation()
        
        return dict(
            title   = "View notification",
            layout  = layout,
            message = "Only the appointed user can view the notification (and we don't think that's you sorry)",
        )
    
    handler = config['handlers'][the_notification.category].handler
    data = the_notification.data
    lib.delete(the_notification)
    
    return handler(request, data)
