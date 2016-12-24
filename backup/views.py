from .models import VM
from .serializers import VMSerializer
from django.contrib.auth.models import User
#from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework import status
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from . import models, utils, utilsH, utilsK, utilsKB, backup_kvm, backup_hyperv, backup_esx


def listESX(request):
    list_VM = utils.main()
    context = {'all_vm': list_VM}
    """for vm in list_VM:
    		VM(VM_name=vm[0], 
    			hyper_type="ESX",
    			disk_location=vm[1],
    			guest_name=vm[2],
    			state=vm[3],
    			ip=vm[6],
    			).save()"""
    		
    return render(request, 'backup/index.html', context)


def listKVM(request):
    list_VM = utilsK.main()
    context = {'all_vm': list_VM}
    for vm in list_VM:
    		"""VM(VM_name=vm[1], 
    			hyper_type="KVM",
    			state=vm[2],
    			disk_location="",
    			guest_name="",
    			ip="",
    			backup_content="",
    			owner=
    			).save()"""
    return render(request, 'backup/hyperKlist.html', context)

def listHyperV(request):
    list_VM = utilsH.main()
    context = {'all_vm': list_VM}
    return render(request, 'backup/hyperVlist.html', context)


def listKVMBackups(request):
    list_VM = utilsKB.main()
    context = {'all_vm': list_VM}
    return render(request, 'backup/hyperKlist.html', context)


def backupKVM(request):
    backup_id = backup_kvm.main()
    context = {'backup_id': backup_id}    		
    return render(request, 'backup/backup_kvm.html', context)

def backupHyperV(request):
	string=backup_hyperv.main()
	context={'status':string}
	return render(request, 'backup/backup_hyperv.html', context)

def backupESX(request):
	string=backup_esx.main()
	context={'status':string}
	return render(request, 'backup/backup_esx.html', context)
