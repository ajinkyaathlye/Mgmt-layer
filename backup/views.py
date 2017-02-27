from .serializers import VMSerializer, ProfileSerializer, JobsSerializer
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from . import models, utils, utilsH, utilsK, utilsKB, backup_kvm, backup_hyperv, backup_esx, apis
from django.http import HttpResponse
import urlparse
import json
from django.views.decorators.csrf import csrf_exempt


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


def getdetails(request, hyper):
    if hyper=="kvm":
        if models.Details.objects.filter(hyper_type="KVM").exists():
            details=models.Details.objects.get(hyper_type="KVM")
            return HttpResponse(details.ip_addr+"$$"+details.username+"$$"+details.password)
        else:
            return HttpResponse("NOT FOUND")
    elif hyper=="esx":
        if models.Details.objects.filter(hyper_type="ESX").exists():
            details = models.Details.objects.get(hyper_type="ESX")
            return HttpResponse(details.ip_addr + "$$" + details.username + "$$" + details.password)
        else:
            return HttpResponse("NOT FOUND")
    elif hyper=="hyperv":
        if models.Details.objects.filter(hyper_type="HyperV").exists():
            details = models.Details.objects.get(hyper_type="HyperV")
            return HttpResponse(details.ip_addr + "$$" + details.username + "$$" + details.password)
        else:
            return HttpResponse("NOT FOUND")


@csrf_exempt
def restore(request, hyper, values):
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    temp = "http://www.dbz.com/goku?"
    temp = temp + values
    print values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    print parsed_dict
    if hyper == 'kvm':
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

    if hyper == 'hyperv':
        if request.method == 'POST':
            bkupname=parsed_dict['backupname'][0]
            #print bkupname
            bkupid=models.Backup.objects.get(backup_name=bkupname).bkupid
            #print bkupid
            vm=models.Backup.objects.get(backup_name=bkupname).vm
            vmid=vm.VM_id
            #print vmid
            resp = apis.vm_list(request,hyper,'restore', vm.details.ip_addr, vm.details.password, vm.details.username, vmid,
                            bkupid)
            return HttpResponse(resp.data)

    if hyper == 'esx':
        if request.method == 'POST':
            bkupname = parsed_dict['backupname'][0]
            # print bkupname
            vm = models.Backup.objects.get(backup_name=bkupname).vm
            vmid = vm.VM_id
            # print vmid
            resp = apis.vm_list(request, hyper, 'restore', vm.details.ip_addr, vm.details.password, vm.details.username,
                                vmid, bkupname)
            return HttpResponse(resp.data)


@csrf_exempt
def configShow(request, hyper, values):
    """Parses the URL-appended data and calls the functions which make the REST api calls"""
    temp = "http://www.dbz.com/goku?"
    temp = temp + values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    #print parsed_dict
    if hyper == 'hyperv':
        if request.method == 'GET':
            #print parsed_dict['servip'][0].strip('/'), parsed_dict['servpaswd'][0], parsed_dict['servuser'][0]
            var = apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0].strip('/'),
                               parsed_dict['servpaswd'][0], parsed_dict['servuser'][0], "")
            #print json.dumps(var.data)
            return HttpResponse(json.dumps(var.data))
        elif request.method == 'POST':
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
            apis.vm_list(request, hyper, "backup", parsed_dict['servip'][0].strip('/'), parsed_dict['servpaswd'][0],
                         parsed_dict['servuser'][0], "")
            return HttpResponse("")


def createPolicy(request, values):
    """Creates a policy and stores it into the database"""
    temp = "http://www.dbz.com/goku?"  # Don't change this, otherwise the code won't work. The power of this url is over 9000!
    temp = temp + values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    if request.method == 'GET':
        var = apis.createPolicy(request, parsed_dict['startDay'][0], parsed_dict['startMonth'][0],
                                parsed_dict['startYear'][0], parsed_dict['endDay'][0], parsed_dict['endMonth'][0],
                                parsed_dict['endYear'][0], parsed_dict['bckrotation'][0], parsed_dict['policyName'][0])
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
    temp = "http://www.dbz.com/vegeta?"
    temp = temp + values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    print parsed_dict
    if request.method == 'GET':
        print parsed_dict['policyName'][0].strip('/')
        apis.conPolicy(request, parsed_dict['policyName'][0].strip('/'), parsed_dict['vmID'][0].strip('/'))
        return HttpResponse("")


def listBackups(request, hyper, values):
    """Lists the backups for a particular VM."""
    temp = "http://www.dbz.com/gohan?"
    temp = temp + values
    parsed = urlparse.urlparse(temp)
    parsed_dict = urlparse.parse_qs(parsed.query)
    #print "Parsed Dict: ", parsed_dict['VMName'][0].strip('/')
    if request.method == 'GET':
            var = apis.vm_list(request, hyper, "restore", parsed_dict['servip'][0].strip('/'),
                               parsed_dict['servpaswd'][0], parsed_dict['servuser'][0],
                               parsed_dict['VMName'][0].strip('/'))
            #print "LIST BACKUPS: ", var
            return HttpResponse(json.dumps(var.data))


def jobDetails(request):
    jobs=models.Jobs.objects.all()
    ord_dict = JobsSerializer(jobs, many=True)
    JSON = json.dumps(ord_dict.data)
    return HttpResponse(JSON)


def jobs(request):
    return render(request, 'backup/jobs.html')


def homePG(request):
    return render(request, 'backup/homePg.html')
