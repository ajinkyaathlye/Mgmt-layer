from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse
#from rest_framework.schemas import get_schema_view
from backup import views
from backup import multi
from backup import global_variables as gv
import sys
import logging

logging.basicConfig(filename='server.log',level=logging.INFO)
logger = logging.getLogger('log')
handler = logging.FileHandler('server.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
#schema_view = get_schema_view(title='Pastebin API')
#print sys.argv
if sys.argv[1] == 'runserver':
	multi.main()

gv.server_ip = sys.argv[-1]
#print gv.server_ip

urlpatterns = [
    # url(r'^$',HttpResponse()),
    #url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('backup.urls')),
  #  url('^schema/$', schema_view),
    #   url(r'^users/$', user_list, name='user-list'),
    #   url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    #   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]