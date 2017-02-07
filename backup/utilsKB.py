import os
import requests
import json


def get_token():
	headers = {'Content-Type': 'application/json',}

	data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "demo", "password":"root123"}}}'

	response=requests.post('http://10.136.60.38:5000/v2.0/tokens', headers=headers, data=data)

	parsed_response=json.loads(response.text)

	token=parsed_response['access']['token']['id']

	#print token
	return token

def list_vms():
	headers = {
    'User-Agent': 'python-novaclient',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(),}
	response=requests.get('http://10.136.60.48:8774/v2.1/f8391ff92c6a4b45b0360f8c85eacb2f/servers/detail', headers=headers)
	parsed_json_response=json.loads(response.text)
	vmlist=[]
	for i in range(len(parsed_json_response['servers'])):
		vm=[]
		vm.append(str(parsed_json_response['servers'][i]['id']))#ID
		vm.append(str(parsed_json_response['servers'][i]['name']))#Name
		vm.append(str( parsed_json_response['servers'][i]['status']))#Status
		
		
		"""print parsed_json_response['servers'][i]['id']
		print parsed_json_response['servers'][i]['name']
		print parsed_json_response['servers'][i]['status']"""
		if parsed_json_response['servers'][i]['OS-EXT-STS:power_state']==1:
			vm.append("Running")#POWER_STATE
			#print "Running"
		else:
			vm.append("OFF")#POWER_STATE
			#print "OFF" 
		if 'private' in parsed_json_response['servers'][i]['addresses']:
			ipv4=parsed_json_response['servers'][i]['addresses']['private'][0]['addr']
			ipv6=parsed_json_response['servers'][i]['addresses']['private'][1]['addr']
			vm.append("Private "+str(ipv4)+" "+str(ipv6)) #NETWORK
			#print "Private",ipv4," ",ipv6
		else:
			ipv4=parsed_json_response['servers'][i]['addresses']['public'][0]['addr']
			ipv6=parsed_json_response['servers'][i]['addresses']['public'][1]['addr']
			vm.append("Private "+str(ipv4)+" "+str(ipv6)) #NETWORK
			#print "Public",ipv4," ",ipv6
		#print vm
		vmlist.append(vm)
		#print "======================================================================="
		
	#print vmlist
	return vmlist
		
def list_backups():
	headers = {
    'User-Agent': 'python-novaclient',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(),
	}
	response=requests.get('http://10.136.60.48:8774/v2.1/f8391ff92c6a4b45b0360f8c85eacb2f/images/detail', headers=headers)
	parsed_json_response=json.loads(response.text)
	backupList=[]
	for i in range(len(parsed_json_response['images'])):
		backup=[]
		backup.append(str(parsed_json_response['images'][i]['id']))#ID
		backup.append(str(parsed_json_response['images'][i]['name']))#Name
		backup.append(str(parsed_json_response['images'][i]['status']))#Status
		
		
		#print "ID",parsed_json_response['images'][i]['id']
		#print "Name",parsed_json_response['images'][i]['name']
		#print "Status",parsed_json_response['images'][i]['status']
		if 'server' in parsed_json_response['images'][i]:
			backup.append("VM ID"+str(parsed_json_response['images'][i]['server']['id']))#VM ID
		else:
			backup.append("VM ID --")#VM ID
			#print "VM ID","--"
		#print backup
		#print "======================================================"
		backupList.append(backup)
	#print backupList
	return backupList
	
	
def backupvm():
	headers = {
    'User-Agent': 'python-novaclient',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(),
}

	data = '{"createBackup": {"backup_type": "daily", "rotation": "1", "name": "testbkup"}}'

	response=requests.post('http://10.136.60.48:8774/v2.1/f8391ff92c6a4b45b0360f8c85eacb2f/servers/ff587d41-0c91-4648-81e6-d74fa6f34615/action', headers=headers, data=data)
	print response.text
	print response
	

def restoreVM():
	headers = {
    'User-Agent': 'python-novaclient',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': 'c56111d47341486fac961de01cc04846',
}

	data = '{"server": {"name": "testcode", "imageRef": "fe800404-88cf-4e03-b2df-888695f79ba2", "availability_zone": "nova", "flavorRef": "1", "max_count": 1, "min_count": 1, "networks": [{"uuid": "140687a0-dd64-4a98-839c-0b032d2c07c2"}], "security_groups": [{"name": "default"}]}}'

	response=requests.post('http://10.136.60.48:8774/v2.1/f8391ff92c6a4b45b0360f8c85eacb2f/servers', headers=headers, data=data)
	parsed_json_response=json.loads(response.text)
	print "Backup restoring with id : ",parsed_json_response['server']['id']
#list_backups()

def main():		
	return list_backups()
#backupvm()


#list_backups()

#restoreVM()