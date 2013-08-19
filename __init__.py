def includeme(config):
    from . import views
    
    """
    Pass this to your configurator object like so:
    
    from . import communique
    config.include(communique, route_prefix="communique")
    """
    
    # Standard views
    config.add_route('communique.home', '/home')
    
    # Now link the views
    config.add_view(views.home, route_name='communique.home', renderer='templates/home.pt', permission='loggedin')
    
    return config
