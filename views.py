import transaction
import datetime

from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer

from .lib import (
    db_funcs,
    actions,
    rules,
)

from .models import (
    ConnectFourGame,
    ConnectFourMove,
)

from .config import config

def menu(request):
    the_user = config['get_user_func'](request)
    layout = get_renderer(config['layout']).implementation()
    
    return dict(
        title        = "Communique",
        layout       = layout,
        the_user     = the_user,
    )
