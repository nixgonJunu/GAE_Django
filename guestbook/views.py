from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect

from google.appengine.api import users

from guestbook.models import Greeting

import urllib

def main_page(request):
    # GET method ('key', 'value')
    guestbook_name = request.GET.get('guestbook_name', 'default_guestbook')
    # get key
    guestbook_key = Greeting.get_key_from_name(guestbook_name)
    # make query for select data ordered dsec
    greetings_query = Greeting.all().ancestor(guestbook_key).order('-date')
    # get result set
    greetings = greetings_query.fetch(10)
    
    # get user, if exist current user
    if users.get_current_user():
        # create logout url
        url = users.create_logout_url(request.get_full_path())
        url_linktext = 'Logout'
    else:
        # create login url
        url = users.create_login_url(request.get_full_path())
        url_linktext = 'Login'
        
    # set up values for use in template
    template_values = {
        'greetings': greetings,
        'guestbook_name': guestbook_name,
        'url': url,
        'url_linktext': url_linktext,
    }
    
    return direct_to_template(request, 'guestbook/main_page.html', template_values)

def sign_post(request):
    if request.method == 'POST':
        guestbook_name = request.POST.get('guestbook_name')
        guestbook_key = Greeting.get_key_from_name(guestbook_name)
        # get DB
        greeting = Greeting(parent=guestbook_key)
    
        # set author
        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()
    
        # set content
        greeting.content = request.POST.get('content')
        # put to DB
        greeting.put()
        
        # return guestbook page by GET METHOD
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    
    return HttpResponseRedirect('/')