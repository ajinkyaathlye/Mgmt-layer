import os
import requests
import json
import logging

logger = logging.getLogger('log')

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


def getVMdetails(ip, username, password, VMID):
    # parameters: ip,user,pass,vmid
    headers = {
        'User-Agent': 'python-novaclient',
        'Accept': 'application/json',
        'X-OpenStack-Nova-API-Version': '2.25',
        'X-Auth-Token': get_token(ip, username, password),
    }

    response = requests.get('http://' + ip + ':8774/v2.1/' + getProjectID(ip) + '/servers/' + VMID, headers=headers,
                            timeout=10)
    logger.info(response.text)
    print response.text
    parsed_response = json.loads(response.text)

    # print parsed_response
    """print parsed_response['server']['OS-EXT-AZ:availability_zone']
	print parsed_response['server']['flavor']['id']
	if ('private'in parsed_response['server']['addresses']):
		print parsed_response['server']['addresses']['private'][1]['addr']
	elif ('public'in parsed_response['server']['addresses']):
		print parsed_response['server']['addresses']['public'][1]['addr']
	print parsed_response['server']['security_groups'][0]['name']"""

    dict = {}
    dict['availability_zone'] = parsed_response['server']['OS-EXT-AZ:availability_zone']
    dict['flavorRef'] = parsed_response['server']['flavor']['id']
    if ('private' in parsed_response['server']['addresses']):
        dict['uuid'] = getNetworkID(ip, username, password,
                                    parsed_response['server']['addresses']['private'][1]['addr'])
    elif ('public' in parsed_response['server']['addresses']):
        dict['uuid'] = getNetworkID(parsed_response['server']['addresses']['public'][1]['addr'])

    dict['security_groups'] = parsed_response['server']['security_groups'][0]['name']
    return dict


def getSubnetID(ip, username, password, address):
    headers = {
        'User-Agent': 'python-neutronclient',
        'Accept': 'application/json',
        'X-Auth-Token': get_token(ip, username, password),
    }

    response = requests.get('http://' + ip + ':9696/v2.0/ports.json', headers=headers, timeout=10)
    logger.info(response.text)
    # print response.text
    parsed_response = json.loads(response.text)
    ports = parsed_response['ports']
    for gg in ports:
        for lol in gg['fixed_ips']:
            if lol['ip_address'] == address:
                return lol['subnet_id']


def getNetworkID(ip, username, password, address):
    headers = {
        'User-Agent': 'python-neutronclient',
        'Accept': 'application/json',
        'X-Auth-Token': get_token(ip, username, password),
    }

    response = requests.get('http://' + ip + ':9696/v2.0/networks.json', headers=headers, timeout=10)
    logger.info(response.text)
    parsed_response = json.loads(response.text)
    subid = getSubnetID(ip, username, password, address)
    for gg in parsed_response['networks']:
        if subid in gg['subnets']:
            return gg['id']


# ff587d41-0c91-4648-81e6-d74fa6f34615	= VM_ID
# str(models.Backup.objects.get(backup_name='Monday 20 February 2017 12:44:19 PM').vm.VM_id)
# models.Backup.objects.get(backup_name='Monday 20 February 2017 12:44:19 PM').bkupid
def restoreVM(ip, username, password, VMID, bkupid, VMNAME):
    headers = {
        'User-Agent': 'python-novaclient',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-OpenStack-Nova-API-Version': '2.25',
        'X-Auth-Token': get_token(ip, username, password),
    }
    print VMNAME
    print bkupid
    dict = getVMdetails(ip, username, password, VMID)
    data = '{"server": {"name": "' + VMNAME + '", "imageRef": "' + bkupid + '", "availability_zone": "' + \
           dict['availability_zone'] + '", "flavorRef": "' + dict[
               'flavorRef'] + '", "max_count": 1, "min_count": 1, "networks": [{"uuid": "' + dict[
               'uuid'] + '"}], "security_groups": [{"name": "' + dict['security_groups'] + '"}]}}'
    print data
    print 'http://' + ip + ':8774/v2.1/' + getProjectID(ip) + '/servers'

    response = requests.post('http://' + ip + ':8774/v2.1/' + getProjectID(ip) + '/servers', headers=headers,
                             data=data, timeout=10)
    logger.info(response.text)

    if response.status_code in [200,201,202] == False:
        return str(response)
    else:
        print response.text
        parsed_json_response = json.loads(response.text)
        print "Backup restoring with id : ", parsed_json_response['server']['id']
        return "Backup restoring with id : ", parsed_json_response['server']['id']


# get_token()
# list_vms()
# list_backups()
# backupvm()


# list_backups()
def main(ip, username, password, VMID, bkupid, VMNAME):
    return restoreVM(ip, username, password, VMID, bkupid, VMNAME)

