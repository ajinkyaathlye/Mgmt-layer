from .models import VM
from .serializers import VMSerializer, ProfileSerializer
from django.contrib.auth.models import User
# from .serializers import UserSerializer
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
from . import models, utils, utilsH, utilsK, utilsKB, backup_kvm, backup_hyperv, backup_esx, apis
from django.http import HttpResponse
import urlparse
import json
from . import global_variables as gv
from django.views.decorators.csrf import csrf_exempt


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
    string = backup_hyperv.main()
    context = {'status': string}
    return render(request, 'backup/backup_hyperv.html', context)


def backupESX(request):
    context = {'status': string}
    return render(request, 'backup/backup_esx.html', context)


def config(request, hyper):
    """"Config calls URL for listing and Backup"""
    if hyper == "hyperv":
        print "ONLY CONFIG"
        return render(request, 'backup/configH.html')

    if hyper == "esx":
        print "ONLY ESX"
        return render(request, 'backup/configE.html')

    if hyper == "kvm":
        print "ONLY CONFIG"
        return render(request, 'backup/configK.html')
@csrf_exempt
def restore(request, hyper, values):
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    temp = "http://www.dbz.com/goku?"
    temp = temp + values
    print values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    print parsed_dict
    if hyper=='kvm':
        if request.method == 'POST':
            bkupname=parsed_dict['backupname'][0]
            #print bkupname
            bkupid=models.Backup.objects.get(backup_name=bkupname).bkupid
            #print bkupid
            vm=models.Backup.objects.get(backup_name=bkupname).vm
            vmid=vm.VM_id
            #print vmid

        resp=apis.vm_list(request,hyper,'restore', vm.details.ip_addr , vm.details.password ,vm.details.username , vmid , bkupid ,parsed_dict['vmname'][0])

    return HttpResponse(resp.data)

@csrf_exempt
def configShow(request, hyper, values):
    """Calls the functions which makes the REST api calls"""
    temp = "http://www.dbz.com/goku?"
    temp = temp + values
    print values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    print parsed_dict
    if hyper == 'hyperv':
        if request.method == 'GET':
            #print parsed_dict['servip'][0].strip('/'), parsed_dict['servpaswd'][0], parsed_dict['servuser'][0]
            var = apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0].strip('/'),
                               parsed_dict['servpaswd'][0], parsed_dict['servuser'][0], "")
            print json.dumps(var.data)
            return HttpResponse(json.dumps(var.data))
        elif request.method == 'POST':
            gv.hyperv_vmID = parsed_dict['vmID'][0].strip('/')
            apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0].strip('/'), parsed_dict['servpaswd'][0],
                         parsed_dict['servuser'][0], "")
            return HttpResponse("")
    elif hyper == 'esx':
        if request.method == 'GET':
            print parsed_dict['servip'][0], parsed_dict['servpaswd'][0], parsed_dict['servuser'][0].strip('/')
            var = apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0], parsed_dict['servpaswd'][0],
                               parsed_dict['servuser'][0].strip('/'), "")
            return HttpResponse(json.dumps(var.data))
        elif request.method == 'POST':
            apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0], parsed_dict['servpaswd'][0],
                         parsed_dict['servuser'][0], "")
            return HttpResponse("")
    elif hyper == 'kvm':
        if request.method == 'GET':
            var = apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0].strip('/'),
                               parsed_dict['servpaswd'][0], parsed_dict['servuser'][0], "")
            print json.dumps(var.data)
            return HttpResponse(json.dumps(var.data))
        elif request.method == 'POST':
            print "ASFASDSADSAD"
            apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0].strip('/'), parsed_dict['servpaswd'][0],
                         parsed_dict['servuser'][0], "")
            # print parsed_dict['servip'][0].strip('/'), parsed_dict['servpaswd'][0], parsed_dict['servuser'][0], parsed_dict['startDate'][0].strip('/'), parsed_dict['endDate'][0].strip('/'), parsed_dict['rotationCount'][0].strip('/')
            return HttpResponse("")


def createPolicy(request, values):
    temp = "http://www.dbz.com/goku?"  # Don't change this, otherwise the code won't work. The power of this url is over 9000!
    temp = temp + values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    if request.method == 'GET':
        var = apis.createPolicy(request, parsed_dict['startDay'][0], parsed_dict['startMonth'][0],
                                parsed_dict['startYear'][0], parsed_dict['endDay'][0], parsed_dict['endMonth'][0],
                                parsed_dict['endYear'][0], parsed_dict['bckrotation'][0])
        return HttpResponse(json.dumps(var.data))


def listPolicies(request):
    """Fetches policies as a JSON list from the database and returns a list"""
    policies = models.Profile.objects.all()
    ord_dict = ProfileSerializer(policies, many=True)
    JSON = json.dumps(ord_dict.data)
    print JSON
    return HttpResponse(JSON)


def connectPolicy(request, hyper, values):
    """Connects a policy to a VM in the database"""
    print "AHAAHAHAHAHAHAHAH"
    temp = "http://www.dbz.com/vegeta?"
    temp = temp + values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    print parsed_dict
    if hyper == 'kvm':
        if request.method == 'GET':
            apis.conPolicy(request, parsed_dict['policyID'][0].strip('/'), parsed_dict['vmID'][0].strip('/'))
            return HttpResponse("")


def listBackups(request, hyper, values):
    """Lists the backups for a particular VM."""
    temp = "http://www.dbz.com/gohan?"
    temp = temp + values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    if hyper == 'kvm':
        if request.method == 'GET':
            var = apis.vm_list(request, hyper, "restore", parsed_dict['servip'][0].strip('/'),
                               parsed_dict['servpaswd'][0], parsed_dict['servuser'][0],
                               parsed_dict['VMName'][0].strip('/'))
            return HttpResponse(json.dumps(var.data))

