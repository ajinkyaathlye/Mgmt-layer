from . import models, backup_kvm
import datetime
from django.views.decorators.csrf import csrf_exempt
import requests
import threading
import global_variables as gv
flag = 0

# DEFINE THREAD CLASS AND FUNCTION
class newThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        check_HyperV()  # function call by Try block in main()

@csrf_exempt
def check_KVM():
    vms_kvm = models.VM.objects.filter(hyper_type='KVM')
    #print vms_kvm
    d = datetime.date.today()
    dt = datetime.datetime.today()
    headers = {
        'Content-Type': 'application/json',
    }
    for vm in vms_kvm:
        if vm.profile == None:
            print "In NONE: ", vm
            pass
        else:

            if d >= vm.profile.start_date and d <= vm.profile.end_date:
                l = models.Backup.objects.filter(vm=vm).order_by('timestamp')
                data = '{"VM_name": "' + vm.VM_id + '", "backup_name":"' + dt.strftime("%A %d %B %Y %I:%M:%S %p") + '"}'
                if len(l) == 0:
                    #print l
                    response = requests.post('http://' + gv.server_ip + '/vm/kvm/backup/servip=' + vm.details.ip_addr +
                                             '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                             headers=headers, data=data)
                else:
                    backup = l[len(l) - 1]
                    #print l
                    print backup
                    # print type(backup.timestamp), type(dt)
                    print (dt - backup.timestamp).days
                    if (dt - backup.timestamp).days == 0:
                        pass
                    else:
                        requests.post('http://' + gv.server_ip + '/vm/kvm/backup/servip=' + vm.details.ip_addr +
                                      '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                      headers=headers, data=data)


def check_ESX():
    vms_esx = models.VM.objects.filter(hyper_type='ESX')
    print vms_esx
    d = datetime.date.today()
    dt = datetime.datetime.today()
    headers = {
        'Content-Type': 'application/json',
    }
    for vm in vms_esx:
        if vm.profile == None:
            #print vm
            pass
        else:

            if d >= vm.profile.start_date and d <= vm.profile.end_date:
                l = models.Backup.objects.filter(vm=vm).order_by('timestamp')
                data = '{"VM_name": "' + vm.VM_id + '", "backup_name":"' + dt.strftime("%A %d %B %Y %I:%M:%S %p") + '"}'
                if len(l) == 0:
                    #print l
                    response = requests.post('http://' + gv.server_ip + '/vm/esx/backup/servip=' + vm.details.ip_addr +
                                             '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                             headers=headers, data=data)
                    #print data
                    print "In L=0:"
                    print "================================="
                    print '/vm/esx/backup/servip=' + vm.details.ip_addr + '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password
                else:
                    backup = l[len(l) - 1]
                    # print l
                    print "++++++++++++++In L != 0: ++++++++++++"
                    print backup
                    # print type(backup.timestamp), type(dt)
                    print (dt - backup.timestamp).days
                    if (dt - backup.timestamp).days == 0:
                        pass
                    else:
                        requests.post('http://' + gv.server_ip + '/vm/esx/backup/servip=' + vm.details.ip_addr +
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
    global flag
    for vm in vms_hyperv:
        if vm.profile == None:
            #print vm
            pass
        else:
            if d >= vm.profile.start_date and d <= vm.profile.end_date:
                l = models.Backup.objects.filter(vm=vm).order_by('timestamp')
                data = '{"VM_name": "' + vm.VM_id + '", "backup_name":"' + dt.strftime("%A %d %B %Y %I:%M:%S %p") + '"}'
                if len(l) == 0:
                    print l
                    flag = 1
                    response = requests.post('http://' + gv.server_ip + '/vm/hyperv/backup/servip=' + vm.details.ip_addr +
                                             '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                             headers=headers, data=data)
                    print data
                    print "================================="
                    print 'http://127.0.0.1:8000/vm/hyperv/backup/servip=' + vm.details.ip_addr + '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password
                else:
                    backup = l[len(l) - 1]
                    #print l
                    print backup
                    # print type(backup.timestamp), type(dt)
                    print (dt - backup.timestamp).days
                    if (dt - backup.timestamp).days == 0:
                        pass
                    else:
                        flag = 1
                        requests.post('http://' + gv.server_ip + '/vm/hyperv/backup/servip=' + vm.details.ip_addr +
                                      '&servuser=' + vm.details.username + '&servpaswd=' + vm.details.password,
                                      headers=headers, data=data)
    flag = 0

def main():
    check_KVM()
    hypThread = newThread(3, "HyperV Thread")
    try:
        if flag == 0:
            hypThread.start()
    except (SystemExit):
        print "cyka blyat"
    check_ESX()

