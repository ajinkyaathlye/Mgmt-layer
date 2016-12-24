import os
import requests
import json


def get_token():
	headers = {'Content-Type': 'application/json',}

	data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "demo", "password":"root123"}}}'

	response=requests.post('http://10.136.60.48:5000/v2.0/tokens', headers=headers, data=data)

	parsed_response=json.loads(response.text)

	token=parsed_response['access']['token']['id']

	#print token
	return token

		
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
	print backupList
	return backupList
	
#ff587d41-0c91-4648-81e6-d74fa6f34615	= VM_ID
	

def restoreVM():
	headers = {
    'User-Agent': 'python-novaclient',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(),
}

	data = '{"server": {"name": "djangoRestore", "imageRef": "fe800404-88cf-4e03-b2df-888695f79ba2", "availability_zone": "nova", "flavorRef": "1", "max_count": 1, "min_count": 1, "networks": [{"uuid": "4a985365-c999-41c7-ae17-0b7929f19009"}], "security_groups": [{"name": "default"}]}}'

	response=requests.post('http://10.136.60.48:8774/v2.1/f8391ff92c6a4b45b0360f8c85eacb2f/servers', headers=headers, data=data)
	parsed_json_response=json.loads(response.text)
	print "Backup restoring with id : ",parsed_json_response['server']['id']

#get_token()	
#list_vms()
#list_backups()
#backupvm()


#list_backups()
def main():
	restoreVM()