from . import models, backup_kvm
import datetime
from django.views.decorators.csrf import csrf_exempt
import requests


@csrf_exempt
def check_KVM():
    vms_kvm = models.VM.objects.filter(hyper_type='KVM')
    print vms_kvm
    d = datetime.date.today()
    dt = datetime.datetime.today()
    headers = {
        'Content-Type': 'application/json',
    }
    for vm in vms_kvm:
        if vm.profile == None:
            print vm
            pass
        else:

            if d >= vm.profile.start_date and d <= vm.profile.end_date:
                l = models.Backup.objects.filter(vm=vm).order_by('timestamp')
                data = '{"VM_name": "' + vm.VM_id + '", "backup_name":"' + dt.strftime("%A %d %B %Y %I:%M:%S %p") + '"}'
                if len(l) == 0:
                    print l
                    response = requests.post('http://127.0.0.1:8000/vm/kvm/backup/servip=' + vm.details.ip_addr +
                                             '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                             headers=headers, data=data)
                    print data
                    print "================================="
                    print 'http://127.0.0.1:8000/vm/kvm/backup/servip=' + vm.details.ip_addr + '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password
                else:
                    backup = l[len(l) - 1]
                    print l
                    print backup
                    # print type(backup.timestamp), type(dt)
                    print (dt - backup.timestamp).days
                    if (dt - backup.timestamp).days == 0:
                        pass
                    else:
                        requests.post('http://127.0.0.1:8000/vm/kvm/backup/servip=' + vm.details.ip_addr +
                                      '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                      headers=headers, data=data)


def check_ESX():
    vms_esx = models.VM.objects.filter(hyper_type='ESX')
    d = datetime.datetime.today()
    headers = {
        'Content-Type': 'application/json',
    }
    for vm in vms_esx:
        if d >= vm.profile.start_date and d <= vm.profile.end_date:
            l = models.Backup.objects.filter(vm=vm).order_by('timestamp')
            for backup in l:
                if backup.timestamp.days - d.days == 0:
                    pass
                else:
                    data = '{"VM_name": "' + vm.VM_id + '", "backup_name":" ' + backup.backup_name + '"}'
                    requests.post('http://127.0.0.1:8000/vm/esx/backup/servip=' + vm.details.ip_addr +
                                  '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                  headers=headers, data=data)


def check_HyperV():
    vms_hyperv = models.VM.objects.filter(hyper_type='HyperV')
    print vms_hyperv
    d = datetime.date.today()
    dt = datetime.datetime.today()
    headers = {
        'Content-Type': 'application/json',
    }
    for vm in vms_hyperv:
        if vm.profile == None:
            print vm
            pass
        else:

            if d >= vm.profile.start_date and d <= vm.profile.end_date:
                l = models.Backup.objects.filter(vm=vm).order_by('timestamp')
                data = '{"VM_name": "' + vm.VM_id + '", "backup_name":"' + dt.strftime("%A %d %B %Y %I:%M:%S %p") + '"}'
                if len(l) == 0:
                    print l
                    response = requests.post('http://127.0.0.1:8000/vm/hyperv/backup/servip=' + vm.details.ip_addr +
                                             '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                             headers=headers, data=data)
                    print data
                    print "================================="
                    print 'http://127.0.0.1:8000/vm/hyperv/backup/servip=' + vm.details.ip_addr + '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password
                else:
                    backup = l[len(l) - 1]
                    print l
                    print backup
                    # print type(backup.timestamp), type(dt)
                    print (dt - backup.timestamp).days
                    if (dt - backup.timestamp).days == 0:
                        pass
                    else:
                        requests.post('http://127.0.0.1:8000/vm/hyperv/backup/servip=' + vm.details.ip_addr +
                                      '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                      headers=headers, data=data)


def main():
    check_KVM()
    check_HyperV()
