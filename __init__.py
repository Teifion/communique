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
    config.add_route('communique.save_preferences', '/save_preferences')
    config.add_route('communique.view', '/view/{notification_id}')
    
    # Now link the views
    config.add_view(views.home, route_name='communique.home', renderer='templates/home.pt', permission='loggedin')
    config.add_view(views.save_preferences, route_name='communique.save_preferences', permission='loggedin')
    config.add_view(views.view, route_name='communique.view', renderer="string", permission='loggedin')
    
    return config
