import os
import requests
import json
from backup import models
import logging

logger = logging.getLogger('log')

# ip="10.136.60.38"

def get_token(ip, username, password):
    """Get Openstack authentication token for all request opertaions"""

    headers = {'Content-Type': 'application/json', }

    data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "' + username + '", "password":"' + password + '"}}}'

    response = requests.post('http://' + ip + ':5000/v2.0/tokens', headers=headers, data=data, timeout=10)
    logger.info(response.text)
    parsed_response = json.loads(response.text)

    token = parsed_response['access']['token']['id']

    # print token
    return token


def getBackupIDbyName(bkupname, ip, username, password):
    """Get Openstack Backup ID given backup name """

    headers = {
        'User-Agent': 'python-novaclient',
        'Accept': 'application/json',
        'X-OpenStack-Nova-API-Version': '2.25',
        'X-Auth-Token': get_token(ip, username, password),
    }
    string = 'http://' + ip + ':8774/v2.1/' + str(getProjectID(ip)) + '/images/detail'
    # print string
    response = requests.get(string, headers=headers, timeout=10)
    logger.info(response.text)
    parsed_json_response = json.loads(response.text)
    backupList = []
    for i in range(len(parsed_json_response['images'])):
        if str(parsed_json_response['images'][i]['name']) == bkupname:
            print str(parsed_json_response['images'][i]['id'])
            return str(parsed_json_response['images'][i]['id'])

    return ""


def deleteBackup(bkupID, ip, username, password):
    """Delete backup using BackupID"""

    headers = {
        'User-Agent': 'python-novaclient',
        'Accept': 'application/json',
        'X-OpenStack-Nova-API-Version': '2.25',
        'X-Auth-Token': get_token(ip, username, password),
    }

    requests.delete('http://' + ip + ':8774/v2.1/' + getProjectID(ip) + '/images/' + bkupID, headers=headers, timeout=10)
    #logger.info(response.text)

def backupvm(ip, backup_name, vm_id, rot_cnt, username, password):
    """"Backup VM using VM-ID"""

    headers = {
        'User-Agent': 'python-novaclient',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-OpenStack-Nova-API-Version': '2.25',
        'X-Auth-Token': get_token(ip, username, password),
    }

    data = '{"createBackup": {"backup_type": "weekly", "rotation": "100", "name":' + '"' + backup_name + '"' + '}}'

    response = requests.post('http://' + ip + ':8774/v2.1/' + getProjectID(ip) + '/servers/' + vm_id + '/action',
                             headers=headers, data=data, timeout=10)
    logger.info(response.text)
    print data
    print response.text
    print response

    VM = models.VM.objects.filter(hyper_type='KVM', VM_id=vm_id)
    db = models.Backup.objects.filter(vm=VM)
    if (len(db) >= rot_cnt):
        id = getBackupIDbyName(str(db[0]), ip, username, password)
        deleteBackup(id, ip, username, password)
        models.Backup.objects.get(backup_name=str(db[0])).delete()

    return str(response.headers['Location']).split('/')[-1]


def getProjectID(ip):
    headers = {'Content-Type': 'application/json', }

    data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "admin", "password":"root123"}}}'

    response = requests.post('http://' + ip + ':5000/v2.0/tokens', headers=headers, data=data, timeout=10)
    logger.info(response.text)
    parsed_response = json.loads(response.text)

    token = parsed_response['access']['token']['id']
    headers = {
        'User-Agent': 'python-keystoneclient',
        'Accept': 'application/json',
        'X-Auth-Token': token, }
    response = requests.get('http://' + ip + ':35357/v2.0/tenants', headers=headers, timeout=10)
    logger.info(response.text)
    parsed_json_response = json.loads(response.text)
    # print parsed_json_response
    gg = parsed_json_response['tenants']
    for ll in gg:
        if ll['name'] == 'demo':
            # print ll['id']
            return ll['id']


def main(ip, backup_name, vm_id, rot_cnt, username, password):
    return backupvm(ip, backup_name, vm_id, rot_cnt, username, password)

