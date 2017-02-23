import atexit
import argparse
import sys
import time
import ssl
import collections

from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi


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
        empty = []
        # mylogger.error("No snapshots found for {0}".format(vm_name))
        print "No snapshots found for {0}".format(vm_name)
        return empty
        # sys.exit(1)
    d = collections.deque(snapshots)
    all_snapshots = []
    while d:
        snapshot = d.pop()
        all_snapshots.append(snapshot)
        d.extend(reversed(snapshot.childSnapshotList))
    return all_snapshots


# ==================================================================MAIN====================================================================


def main(ip, password, user, VM):
    inputs = {'vcenter_ip': ip,
              'vcenter_password': password,
              'vcenter_user': user,
              'vm_name': VM,
              # create, remove,info,snap info or list
              'operation': 'snap info',
              'snapshot_name': '',
              'ignore_ssl': True
              }
    si = None
    try:
        print "Trying to connect to VCENTER SERVER . . ."

        context = None
        if inputs['ignore_ssl']:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.verify_mode = ssl.CERT_NONE

        # si = connect.Connect(args.host, int(args.port), args.user, args.password, service="hostd")
        si = connect.Connect(inputs['vcenter_ip'], 443, inputs['vcenter_user'], inputs['vcenter_password'],
                             sslContext=context)
    except IOError, e:
        pass
        atexit.register(Disconnect, si)

    print "Connected to VCENTER SERVER !"

    content = si.RetrieveContent()

    operation = inputs['operation']

    vm_name = inputs['vm_name']
    # snapshot_name = inputs['snapshot_name']

    vm = get_obj(content, [vim.VirtualMachine], vm_name)

    # ==================================================BACKUP INFO================================================
    l = []
    if operation == 'snap info':

        all_snapshots = list_snapshot(vm, vm_name)
        if all_snapshots == []:
            print 'No snapshots available'
        for snapshot in all_snapshots:
            a = []
            a.append(snapshot.name)
            a.append(snapshot.createTime)
            l.append(a)
    l = filter(None, l)
    return l
