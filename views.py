import transaction
import datetime

from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer
from pyramid.renderers import render_to_response

from .config import config
from . import lib

def home(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    output = []
    last_was_unread = True
    for i, n in enumerate(lib.get_current(user_id=the_user.id)):
        handler = config['handlers'][n.category]
        
        # Add a spacer between read and unread but only if they're mixed, not if all are read
        if n.read == True and last_was_unread:
            last_was_read = False
            if i > 0:
                output.append("<hr />")
        
        output.append("""
            <a class="communique-notification-row {read}" href="{communique_view}">
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
            read = "communique-notification-read" if n.read else "communique-notification-unread",
        ))
    
    options = list(config['handlers'].keys())
    options.sort()
    
    return dict(
        title         = "Communique",
        layout        = layout,
        the_user      = the_user,
        notifications = "".join(output),
        
        options       = options,
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
    last_was_unread = True
    
    for i, n in enumerate(lib.get_current(user_id=the_user.id)):
        handler = config['handlers'][n.category]
        
        # Add a spacer between read and unread but only if they're mixed, not if all are read
        if n.read == True and last_was_unread:
            last_was_read = False
            if i > 0:
                output.append("<hr />")
        
        output.append("""
            <a class="communique-notification-row {read}" href="{communique_view}">
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
            read = "communique-notification-read" if n.read else "communique-notification-unread",
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
        
        return render_to_response("templates/view.pt",
            dict(
                title   = "View notification",
                layout  = layout,
                message = "We couldn't find that notification!",
            ),
            request = request,
        )
    
    if the_notification.user != the_user.id:
        layout = get_renderer(config['layout']).implementation()
        
        return render_to_response("templates/view.pt",
            dict(
                title   = "View notification",
                layout  = layout,
                message = "Only the appointed user can view the notification (and we don't think that's you sorry)",
            ),
            request = request,
        )
    
    handler = config['handlers'][the_notification.category].handler
    data = the_notification.data
    lib.mark_as_read(the_notification)
    
    return handler(request, data)

def create(request):
    pass