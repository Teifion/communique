from datetime import datetime, timedelta, date
from collections import namedtuple
from .config import config
from .models import Notification
from . import lib
 
NotificationCategory = namedtuple("NotificationCategory", ["name", "label", "icon_path", "handler"])
def register(name, label, icon_path, handler, raise_on_dupe=False):
    """
    Examples:
    register('wordy.new_game', 'New game', 'new_game.png', wordy_game_forward)
    register('wordy.new_move', 'New move', 'new_move.png', wordy_game_forward)
    register('wordy.game_lost', 'Game lost', 'game_lost.png', wordy_view_stats)
    """
   
    if name in config['handlers']:
        if raise_on_dupe:
            raise KeyError("{} already exists".format(name))
        else:
            return False
   
    nc = NotificationCategory(name, label, icon_path, handler)
    config['handlers'][name] = nc
    return True

def send(user, category, message, data, expires=None, posted=None, avoid_duplicates=False):
    """
    Category is the key for the registered notification type
    Message is the message that will be displayed in the rectangle
    Data is a string containing information passed to the handler function (as a string)
    Expires is either the datetime it expires or a timedelta of how long it will last
    Posted allows you to post it to the future
    Avoid duplicates means it will make sure the user doesn't already have a notification of this type before adding it
    
    Examples:
    send(1, "wordy.new_move", "Fred has made a move", "15", timedelta(hours=6))
    send(1, "wordy.new_game", "Bob has started a game with you", "20", timedelta(hours=6))
    send(1, "wordy.game_lost", "Gemma has won the game", "12", timedelta(hours=6))
    """
    
    if category not in config['handlers']:
        raise KeyError("No handler for the communique category of '{}'".format(category))
    
    if avoid_duplicates:
        lib.clear(user, category=category)
        c = lib.count_of_category(user, category)
        if c > 0:
            return False
    
    # If it's a timedelta then convert it to a datetime
    if posted is None:
        posted = datetime.now()
    
    if isinstance(expires, timedelta):
        expires = datetime.now() + expires
    
    # If it's a date then make it a datetime to enusre it'll go into the database fine
    if isinstance(expires, date) and not isinstance(expires, datetime):
        expires = datetime(expires.year, expires.month, expires.day)
    
    # print(expires)
    n = Notification(
        user     = user,
        message  = message,
        category = category,
        data     = data,
        expires  = expires,
        posted   = posted,
    )
    
    config['DBSession'].add(n)

"""
    Javascript and CSS to insert
<script type="text/javascript" charset="utf-8" tal:condition="hasattr(request, 'user')">
    function show_communique_menu ()
    {
        var is_vis = $("#communique-dropdown").is(":visible");
        
        if (is_vis == true)
        {
            $("#communique-dropdown").hide(250);
        }
        else
        {
            $('#communique-dropdown').load(
                '${request.route_url('communique.mini_home')}',
                {},
                function () {
                    $("#communique-dropdown").show(250);
                }
            );
        }
    }
    
    function get_communique_count ()
    {
        $.ajax({
            url: '${request.route_url('communique.home_count', user_id=request.user.id)}',
            type: 'get',
            async: true,
            cache: false,
            success: function(data) {
                if (data != '0')
                {
                    $('#communique-counter').html('(' + data + ')');
                    $('#communique-counter').show(100);
                }
                else
                {
                    $('#communique-counter').hide(100);
                }
            }
        });
    }
    
    $(function() {
        var commuique_menu = "<div id='communique-menu'><a href='${request.route_url("communique.home")}' id='communique-link'>&#9881;</a><div onclick='show_communique_menu();'>Notifications<div id='communique-counter'></div></div><div id='communique-dropdown'></div></div>";
        $('body').prepend(commuique_menu);
        $('#communique-counter').hide();
        
        get_communique_count();
        var intervalID = window.setInterval("get_communique_count();", 60*1000);
    });
</script>

<style type="text/css" media="screen">
    #communique-link
    {
        display:inline-block;
        color: #CCC;
        text-decoration:none;
        float: left;
        padding-right: 10px;
    }
    
    #communique-link:hover
    {
        color: #FFF;
    }
    
    #communique-menu
    {
        background-color:#246;
        color:#FFF;
        position:absolute;
        top:0;
        left:0;
        padding:5px 10px;
        cursor:pointer;
        min-width: 150px;
    }
    
    #communique-counter
    {
        float:right;
        display:inline-block;
        background-color:#702;
        color:#FFF;
        padding:5px 5px;
        margin:-5px -10px -5px 10px;
    }
    
    #communique-dropdown
    {
        display:none;
        margin-top:5px;
        padding-top:5px;
        max-height: 400px;
        border-top:1px solid #000;
    }
    
    .communique-notification-row
    {
        height: 38px;
        margin: 10px 0px;
        min-width: 400px;
        display:block;
        text-decoration:none;
        color: #CCC;
        margin-right:20px;
    }
    
    .communique-notification-row:hover
    {
        color: #FFF;
    }
    
    .communique-notification-read
    {
        color: #888;
    }
    
    .communique-notification-read:hover
    {
        color: #AAA;
    }
    
    .communique-notification-text
    {
        padding-top:5px;
    }
    
    .communique-notification-icon
    {
        width: 32px;
        height: 32px;
        margin-right: 10px;
        float: left;
    }
</style>
"""
