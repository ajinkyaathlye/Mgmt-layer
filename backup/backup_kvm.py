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
	#print backupList
	return backupList
	
	
def backupvm(name):
	headers = {
    'User-Agent': 'python-novaclient',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(),
	}

	data = '{"createBackup": {"backup_type": "daily", "rotation": "2", "name": "' + name + '"}}'

	response=requests.post('http://10.136.60.48:8774/v2.1/f8391ff92c6a4b45b0360f8c85eacb2f/servers/ff587d41-0c91-4648-81e6-d74fa6f34615/action', headers=headers, data=data)
	backupList=list_backups()
	for i in range(len(backupList)):
		if str(name) in backupList[i]:
				return backupList[i]
		else:
			return []


def main(name):		
	return backupvm(name)

#backupvm()


#list_backups()

#restoreVM()