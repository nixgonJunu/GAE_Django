from django.conf.urls.defaults import *
from guestbook.views import main_page, sign_post

# redirect url
urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    (r'^$', main_page),
)