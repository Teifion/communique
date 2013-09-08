from .api import register, send

def includeme(config):
    from . import views
    
    """
    Pass this to your configurator object like so:
    
    from . import communique
    config.include(communique, route_prefix="communique")
    """
    
    # Standard views
    config.add_route('communique.home', '/home')
    config.add_route('communique.action', '/action/{action}')
    config.add_route('communique.view', '/view/{notification_id}')
    config.add_route('communique.mini_home', '/mini_home')
    config.add_route('communique.home_count', '/home_count/{user_id}')
    config.add_route('communique.create', '/create')
    
    # Now link the views
    config.add_view(views.home, route_name='communique.home', renderer='templates/home.pt', permission='loggedin')
    config.add_view(views.action, route_name='communique.action', permission='loggedin')
    config.add_view(views.mini_home, route_name='communique.mini_home', renderer='string', permission='loggedin')
    
    config.add_view(views.home_count, route_name='communique.home_count', renderer='string')
    config.add_view(views.view, route_name='communique.view', renderer="string", permission='loggedin')
    
    # Not sure what you use but this is the dev type permission I've got on my system
    config.add_view(views.create, route_name='communique.create', permission='code')
    
    return config
