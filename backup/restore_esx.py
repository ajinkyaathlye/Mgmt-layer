import atexit
import argparse
import sys
import time
import ssl
import collections

from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi

class NoSnapshot(Exception):
    pass



	
def main(vm_name, backup_name):

	inputs = {'vcenter_ip': '192.168.32.98',
          'vcenter_password': 'gsLab123',
          'vcenter_user': 'sumitt@ad2lab.com',
          'vm_name' : vm_name,
          #create, remove,info,snap info or list
          'operation' : 'create',
          'snapshot_name' : backup_name,   
          'ignore_ssl': True
          }
	si=None
	try:
		#si = None
		vmnames = [vm_name]
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
		print

	  # Retreive the list of Virtual Machines from the inventory objects
	  # under the rootFolder
		content = si.content
		objView = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)
														
		vmList = objView.view
		objView.Destroy()



	  # Find the vm and power it on
		tasks = [vm.PowerOn() for vm in vmList if vm.name in vmnames]
		print tasks
		print("Virtual Machine(s) have been powered on successfully")
		print 
	except vmodl.MethodFault as e:
		print("Caught vmodl fault : " + e.msg)
	except Exception as e:
		print("Caught Exception : " + str(e))
	found=0
	time.sleep(3)
	snapshot_name = backup_name # snapshot name
	for vm in vmList:
		if vm.name in vmnames:
			snapshots = vm.snapshot.rootSnapshotList
			for snapshot in snapshots:
				if snapshot_name == snapshot.name:
					found=1 
					snap_obj = snapshot.snapshot
					print ("Restoring snapshot ", snapshot.name)
					task = [snap_obj.RevertToSnapshot_Task()]
					#print task
					#wait_for_task(task)
					#WaitForTask(task, si)
	if found == 0:
		print
		print 'No Snapshots available to be reverted to'
		raise NoSnapshot("No snapshot found")
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
