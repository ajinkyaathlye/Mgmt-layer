import os
import requests
import json

#ip="10.136.60.38"

def get_token(ip):
	headers = {'Content-Type': 'application/json',}

	data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "demo", "password":"root123"}}}'

	response=requests.post('http://'+ip+':5000/v2.0/tokens', headers=headers, data=data)

	parsed_response=json.loads(response.text)

	token=parsed_response['access']['token']['id']

	#print token
	return token
	
def backupvm(ip, backup_name, vm_id):
	headers = {
    'User-Agent': 'python-novaclient',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-OpenStack-Nova-API-Version': '2.25',
    'X-Auth-Token': get_token(ip),
	}

	data = '{"createBackup": {"backup_type": "daily", "rotation": "10", "name":' + '"' + backup_name + '"' + '}}'

	response=requests.post('http://'+ip+':8774/v2.1/'+getProjectID(ip)+'/servers/'+ vm_id +'/action', headers=headers, data=data)
	print data
	print response.text
	print response
	

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

def main(ip, backup_name, vm_id):
	backupvm(ip, backup_name, vm_id)