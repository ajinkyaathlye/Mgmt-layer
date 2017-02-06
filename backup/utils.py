import atexit
import argparse
import sys
import time
import ssl
import collections
from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi

a = []


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def PrintVmInfo(vm, depth=1):
    maxdepth = 10
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            PrintVmInfo(c, depth + 1)
        return
    if isinstance(vm, vim.VirtualApp):
        vmList = vm.vm
        for c in vmList:
            PrintVmInfo(c, depth + 1)
        return

    summary = vm.summary
    global a
    l=[]
    l.append(summary.config.name)
    if summary.config.vmPathName is not None and summary.config.vmPathName != "":
        l.append(summary.config.vmPathName)
    else:
        l.append("")
    l.append(summary.config.guestFullName)
    l.append(summary.runtime.powerState)
    if summary.guest is not None:
        ip = summary.guest.ipAddress
        if ip is not None and ip != "":
            l.append(summary.guest.ipAddress)
        else:
            l.append("")
    annotation = summary.config.annotation
    if annotation is not None and annotation != "":
        l.append(summary.config.annotation)
    else:
        l.append("")
    if summary.runtime.question is not None:
        l.append(summary.runtime.question)
    else:
        l.append("")
    a.append(l)

def main(ip, password, user):
    global a
    del a[:]
    inputs = {'vcenter_ip': str(ip),
              'vcenter_password': str(password),
              'vcenter_user': str(user),
              'vm_name': "",
              # create, remove,info,snap info or list
              'operation': 'info',
              'snapshot_name': 'testtt',
              'ignore_ssl': True
             }

    si = None
    try:
        # print "Trying to connect to VCENTER SERVER . . ."

        context = None
        if inputs['ignore_ssl']:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.verify_mode = ssl.CERT_NONE

        # si = connect.Connect(args.host, int(args.port), args.user, args.password, service="hostd")
        si = connect.Connect(
            inputs['vcenter_ip'],
            443,
            inputs['vcenter_user'],
            inputs['vcenter_password'],
            sslContext=context)
    except IOError, e:
        pass
        atexit.register(Disconnect, si)

    # print "Connected to VCENTER SERVER !"

    content = si.RetrieveContent()

    operation = inputs['operation']

    vm_name = inputs['vm_name']
    snapshot_name = inputs['snapshot_name']

    vm = get_obj(content, [vim.VirtualMachine], vm_name)

    if operation == 'info':
        for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                datacenter = child
                vmFolder = datacenter.vmFolder
                vmList = vmFolder.childEntity
                for vm in vmList:
                    PrintVmInfo(vm)

    a=filter(None,a)
    return a