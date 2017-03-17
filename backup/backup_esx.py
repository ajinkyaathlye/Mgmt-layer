import atexit
import argparse
import sys
import time
import ssl
import collections
import pdb
from . import models
from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi

a = []


def get_obj(content, vimtype, name):
    """Get the vsphere object associated with a given text name"""
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


# used for task synchronisation.
# si= service instance; pc=property collector; pc gets properties of VMs by connecting to si.
def wait_for_task(task, raiseOnError=True, si=None, pc=None):
    if si is None:
        si = GetSi()

    if pc is None:
        sc = si.RetrieveContent()
        pc = sc.propertyCollector

    # First create the object specification as the task object.(where to look for data)
    objspec = vmodl.Query.PropertyCollector.ObjectSpec()
    objspec.SetObj(task)
    # Next, create the property specification as the state.(what data is needed from VMs)
    propspec = vmodl.Query.PropertyCollector.PropertySpec()
    propspec.SetType(vim.Task);
    propspec.SetPathSet(["info.state"]);
    propspec.SetAll(True)

    # Create a filter spec with the specified object and property spec.(object spec and property spec needs to be combined into filter spec)
    filterspec = vmodl.Query.PropertyCollector.FilterSpec()
    filterspec.SetObjectSet([objspec])
    filterspec.SetPropSet([propspec])

    # Create the filter
    filter = pc.CreateFilter(filterspec, True)

    # Loop looking for updates till the state moves to a completed state.
    taskName = task.GetInfo().GetName()
    update = pc.WaitForUpdates(None)
    state = task.GetInfo().GetState()
    while state != vim.TaskInfo.State.success and \
                    state != vim.TaskInfo.State.error:
        if (state == 'running') and (taskName.info.name != "Destroy"):
            # check to see if VM needs to ask a question, thow exception
            vm = task.GetInfo().GetEntity()
            if vm is not None and isinstance(vm, vim.VirtualMachine):
                qst = vm.GetRuntime().GetQuestion()
            if qst is not None:
                raise Exception("Task blocked, User Intervention required")

    update = pc.WaitForUpdates(update.GetVersion())
    state = task.GetInfo().GetState()

    filter.Destroy()  # filter spec is not destroyed once created
    if state == "error" and raiseOnError:
        raise task.GetInfo().GetError()

    return state


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
    l = []
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


def invoke_and_track(func, *args, **kw):
    try:
        task = func(*args, **kw)  # kw is used to pass variable length keywords as parameters.
        # print type(task)
        wait_for_task(task)
    except Exception as e:
        # print e
        # raise
        pass


# find the path of the backup.
def get_snapshots(vm):
    return get_snapshots_recursively(vm.snapshot.rootSnapshotList, '')


def get_snapshots_recursively(snapshots, snapshot_location):
    snapshot_paths = []

    if not snapshots:
        return snapshot_paths

    for snapshot in snapshots:
        if snapshot_location:
            current_snapshot_path = snapshot_location + '/' + snapshot.name
        else:
            current_snapshot_path = snapshot.name

        snapshot_paths.append(current_snapshot_path)
        snapshot_paths = snapshot_paths + get_snapshots_recursively(snapshot.childSnapshotList, current_snapshot_path)

    return snapshot_paths


def remove(vm, vm_name, snapshot_name):
    all_snapshots = list_snapshot(vm, vm_name)

    for snapshot in all_snapshots:
        if snapshot_name == snapshot.name:
            snap_obj = snapshot.snapshot
            print "Removing snapshot ", snap_obj
            invoke_and_track(snap_obj.RemoveSnapshot_Task(True))
            print "Removed snapshot successfully..."
        else:
            print "Couldn't find any snapshots"


def list_snapshot(vm, vm_name):
    """Lists the snapshots of the VMs Present"""
    all_snapshots = []
    try:
        snapshots = vm.snapshot.rootSnapshotList
    except AttributeError as e:
        # mylogger.error("No snapshots found for {0}".format(vm_name))
        # print "No snapshots found for {0}".format(vm_name)
        # sys.exit(1)
        return all_snapshots
        pass
    d = collections.deque(snapshots)

    while d:
        snapshot = d.pop()
        all_snapshots.append(snapshot)
        d.extend(reversed(snapshot.childSnapshotList))
    return all_snapshots


# ==================================================================MAIN====================================================================


def main(ip, password, user, vm_name, snap_name, rot_cnt):
    string = ""
    inputs = {'vcenter_ip': ip,
              'vcenter_password': password,
              'vcenter_user': user,
              'vm_name': vm_name,  # 'test_TSAM',
              # create, remove,info,snap info or list
              'operation': 'create',
              'snapshot_name': snap_name,
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
        si = connect.Connect(inputs['vcenter_ip'], 443, inputs['vcenter_user'], inputs['vcenter_password'],
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

    # ==================================================CREATE==================================================================================
    if operation == 'create':
        description = "VM Snapshot"
        dumpMemory = False
        quiesce = True
        try:
            snapshots = vm.snapshot.rootSnapshotList
        except AttributeError as e:
            pass
        # print "Snapshot created successfully with the name as: "+snapshot_name
        # pdb.set_trace()
        # invoke_and_track(vm.CreateSnapshot(snapshot_name, description, dumpMemory, quiesce))
        snap_list = list_snapshot(vm, vm_name)
        flag = 0
        for snaps in snap_list:
            if snaps.name == snapshot_name:
                # print "Snapshot with name : "+snapshot_name+" already exists. Please enter a different name"
                flag = 1
                break
        if flag == 0:
            string = "Snapshot created successfully with the name as: " + snapshot_name
            VM = models.VM.objects.filter(hyper_type='ESX', VM_id=vm_name)
            db = models.Backup.objects.filter(vm=VM)
            if (len(db) >= rot_cnt):
                remove(vm, vm_name, db[0].backup_name)
                for d in db:
                    models.Backup.objects.get(backup_name=d.backup_name).delete()
                print "DELETED"
            invoke_and_track(vm.CreateSnapshot(snapshot_name, description, dumpMemory, quiesce))
