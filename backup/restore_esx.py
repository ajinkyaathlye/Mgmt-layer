import atexit
import argparse
import sys
import time
import ssl
import collections
from . import models
from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi

si = None


def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def list_snapshot(vm, vm_name):
    try:
        snapshots = vm.snapshot.rootSnapshotList
    except AttributeError as e:
        # mylogger.error("No snapshots found for {0}".format(vm_name))
        print "No snapshots found for {0}".format(vm_name)
    # sys.exit(1)
    d = collections.deque(snapshots)
    all_snapshots = []
    while d:
        snapshot = d.pop()
        all_snapshots.append(snapshot)
        d.extend(reversed(snapshot.childSnapshotList))
    return all_snapshots


def main(ip, password, user, vmname, backup_name):
    inputs = {'vcenter_ip': ip,
              'vcenter_password': password,
              'vcenter_user': user,
              'vm_name': vmname,
              # create, remove,info,snap info or list
              'operation': 'create',
              'snapshot_name': backup_name,
              'ignore_ssl': True
              }

    try:
        vmnames = []
        vms = models.VM.objects.get(VM_id=vmname)
        vmnames.append(str(vms.VM_id))

        if not len(vmnames):
            print("No virtual machine specified for power-on")
            sys.exit()

        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE

        try:
            global si
            si = connect.Connect(inputs['vcenter_ip'], 443, inputs['vcenter_user'], inputs['vcenter_password'],
                                 sslContext=context)
            print si
        except IOError:
            print 'Connection Error'
            pass
        if not si:
            print("Cannot connect to specified host.......")
            sys.exit()

        atexit.register(Disconnect, si)
        print 'Successfully connected to Vcentre........'
        print inputs['snapshot_name']
        vm_name = inputs['vm_name']
        # Retreive the list of Virtual Machines from the inventory objects
        # under the rootFolder
        content = si.content
        objView = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

        vmList = objView.view
        objView.Destroy()

        # Find the vm and power it on
        #tasks = [vm.PowerOn() for vm in vmList if vm.name in vmnames]
        #print tasks
        #print("Virtual Machine(s) have been powered on successfully")
        #print
    except vmodl.MethodFault as e:
        print("Caught vmodl fault : " + e.msg)
    except Exception as e:
        print("Caught Exception : " + str(e))
    found = 0
    #time.sleep(3)
    vm = get_obj(content, [vim.VirtualMachine], vm_name)
    print vm
    all_snapshots = list_snapshot(vm, vm_name)
    # print all_snapshots
    # snapshot_name = 'Tuesday 21 February 2017 03:34:24 PM'  # snapshot name
    for vm in vmList:
        if vm.name in vmnames:
            snaps = all_snapshots
            for snapshot in snaps:
                if inputs['snapshot_name'] == snapshot.name:
                    found = 1
                    snap_obj = snapshot.snapshot
                    print ("Restoring snapshot ", snapshot.name)
                    task = [snap_obj.RevertToSnapshot_Task()]
                # print task
                # wait_for_task(task)
                # WaitForTask(task, si)
    if found == 0:
        print
        print 'No Snapshots available to be reverted to'
