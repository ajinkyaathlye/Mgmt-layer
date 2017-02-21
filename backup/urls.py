from django.conf.urls import url, include
from . import views,apis
#from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
import pdb

# Create a router and register our viewsets with it.
"""router = DefaultRouter()
router.register('vm', views.VMViewSet)
router.register('users', views.UserViewSet)"""


#app_name='backup'

urlpatterns = [
    url(r'^api/(?P<util>[a-z]+)/(?P<hv>[a-z]+)/list/', apis.vm_list),
    url(r'^api/(?P<util>[a-z]+)/(?P<hv>[a-z]+)/list/(?P<name>[A-Za-z0-9._@-]+)/', apis.vm_detail),
    url(r'^api/policy/', apis.createPolicy),
    url(r'^policy/list/', views.listPolicies, name='listPolicies'),
    url(r'^policy/create/(?P<values>[A-Za-z0-9._@&%=:/,?-]+)', views.createPolicy),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^vm/listesx/', views.listESX, name='listESX'),
    url(r'^vm/listkvm/', views.listKVM, name='listKVM'),
    url(r'^vm/listhyperv/',views.listHyperV, name='listHyperV'),
    url(r'^vm/listkvmbackups/', views.listKVMBackups, name='listKVMBackups'),
    url(r'^vm/backup/kvm',views.backupKVM, name='backupKVM'),
    url(r'^vm/backup/hyperv',views.backupHyperV, name='backupHyperV'),
    url(r'^vm/(?P<hyper>[a-z]+)/backup/(?P<values>[A-Za-z0-9._@&%=:/,?-]+)',views.configShow, name='configShow'),
    url(r'^vm/(?P<hyper>[a-z]+)/listbackups/(?P<values>[A-Za-z0-9._@&%=:/,?-]+)',views.listBackups, name='listbackups'),
    url(r'^config/(?P<hyper>[a-z]+)/$',views.config, name='config'),
    url(r'^vm/(?P<hyper>[a-z]+)/list/(?P<values>[A-Za-z0-9._@&%=:/,?-]+)',views.configShow, name='configShow'),
    url(r'^policy/(?P<hyper>[a-z]+)/(?P<values>[A-Za-z0-9._@&%=:/,?-]+)', views.connectPolicy, name='connectPolicy'),
    url(r'^vm/(?P<hyper>[a-z]+)/restore/(?P<values>[A-Za-z0-9._@&%=:/, ?-]+)',views.restore, name='restore'),
#url(r'^login/$', auth_views.login, name='login')
    #url(r'^', auth_views.login, {'template_name': 'backup/config.html'}, name='login'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
