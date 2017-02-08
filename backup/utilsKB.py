import os
import requests
import json

#ip="10.136.60.38"

def get_token(ip,username,password):

	"""Get Openstack authentication token for all request opertaions"""

	headers = {'Content-Type': 'application/json',}

	data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "'+username+'", "password":"'+password+'"}}}'

	response=requests.post('http://'+ip+':5000/v2.0/tokens', headers=headers, data=data)

	parsed_response=json.loads(response.text)

	token=parsed_response['access']['token']['id']

	#print token
	return token

		
def list_backups(ip, VMID):
	#VMID='9580f46e-2bc3-42af-97bb-8a365ac9de71'
	headers = {
    'User-Agent': 'python-novaclient',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(),
	}
	string='http://'+ip+':8774/v2.1/'+str(getProjectID())+'/images/detail'
	#print string
	response=requests.get(string, headers=headers)
	parsed_json_response=json.loads(response.text)
	backupList=[]
	for i in range(len(parsed_json_response['images'])):
		backup=[]
		if 'server' in parsed_json_response['images'][i]:
			if str(parsed_json_response['images'][i]['server']['id'])!= VMID:
				continue
			backup.append(str(parsed_json_response['images'][i]['id']))#ID
			backup.append(str(parsed_json_response['images'][i]['name']))#Name
			backup.append(str(parsed_json_response['images'][i]['status']))#Status
		else:
			continue
		#print backup
		backupList.append(backup)
	#print backupList
	return backupList


def getProjectID(ip):
	headers = {'Content-Type': 'application/json',}

	data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "admin", "password":"root123"}}}'

	response=requests.post('http://'+ip+':5000/v2.0/tokens', headers=headers, data=data)

	parsed_response=json.loads(response.text)

	token=parsed_response['access']['token']['id']
	headers = {
    'User-Agent': 'python-keystoneclient',
    'Accept': 'application/json',
    'X-Auth-Token': token,}
	response=requests.get('http://'+ip+':35357/v2.0/tenants', headers=headers)
	parsed_json_response=json.loads(response.text)
	#print parsed_json_response
	gg=parsed_json_response['tenants']
	for ll in gg:
		if  ll['name']=='demo':
			#print ll['id']
			return ll['id']

def getVMdetails():
	#parameters: ip,user,pass,vmid
	headers = {
    'User-Agent': 'python-novaclient',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(),
}

	response=requests.get('http://10.136.60.38:8774/v2.1/'+getProjectID()+'/servers/9580f46e-2bc3-42af-97bb-8a365ac9de71', headers=headers)
	#print response.text
	parsed_response=json.loads(response.text)
	#print parsed_response
	"""print parsed_response['server']['OS-EXT-AZ:availability_zone']
	print parsed_response['server']['flavor']['id']
	if ('private'in parsed_response['server']['addresses']):
		print parsed_response['server']['addresses']['private'][1]['addr']
	elif ('public'in parsed_response['server']['addresses']):
		print parsed_response['server']['addresses']['public'][1]['addr']
	print parsed_response['server']['security_groups'][0]['name']"""
	
	dict={}
	dict['availability_zone']=parsed_response['server']['OS-EXT-AZ:availability_zone']
	dict['flavorRef']=parsed_response['server']['flavor']['id']
	if ('private'in parsed_response['server']['addresses']):
		dict['uuid']=parsed_response['server']['addresses']['private'][1]['addr']
	elif ('public'in parsed_response['server']['addresses']):
		dict['uuid']= parsed_response['server']['addresses']['public'][1]['addr']

	dict['security_groups']=parsed_response['server']['security_groups'][0]['name']
	return dict
	

def main():
	getVMdetails()
	#print get_token()	
	#list_vms()
	list_backups()
	#backupvm()
	#deleteBackup()
	#print getBackupIDbyName("Wed Feb 01 2017 12:53:50 GMT+0530 (IST)")
	#list_backups()

	#restoreVM()
	#list_vms()