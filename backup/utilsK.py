import os
import requests
import json
import logging
# ip="10.136.60.38"

logger = logging.getLogger('log')

def get_token(ip, username, password):
    """Get openstack authentication token for all operations"""
    headers = {'Content-Type': 'application/json', }

    # data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "demo", "password":"root123"}}}'
    data = '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "' + username + '", "password":"' + password + '"}}}'

    response = requests.post('http://' + ip + ':5000/v2.0/tokens', headers=headers, data=data, timeout=10)
    logger.info(response.text)
    parsed_response = json.loads(response.text)

    token = parsed_response['access']['token']['id']

    # print token
    return token


def list_vms(ip, username, password):
    """Return list of VMs currently running in project demo for user #username with password #password"""
    headers = {
        'User-Agent': 'python-novaclient',
        'Accept': 'application/json',
        'X-OpenStack-Nova-API-Version': '2.25',
        'X-Auth-Token': get_token(ip, username, password), }

    string = 'http://' + ip + ':8774/v2.1/' + str(getProjectID(ip)) + '/servers/detail'
    print ip
    response = requests.get(string, headers=headers, timeout=10)
    logger.info(response.text)
    #print response
    parsed_json_response = json.loads(response.text)
    vmlist = []
    for i in range(len(parsed_json_response['servers'])):
        vm = []
        vm.append(str(parsed_json_response['servers'][i]['id']))  # ID
        vm.append(str(parsed_json_response['servers'][i]['name']))  # Name
        vm.append(str(parsed_json_response['servers'][i]['status']))  # Status

        """print parsed_json_response['servers'][i]['id']
		print parsed_json_response['servers'][i]['name']
		print parsed_json_response['servers'][i]['status']"""
        if parsed_json_response['servers'][i]['OS-EXT-STS:power_state'] == 1:
            vm.append("Running")  # POWER_STATE
        # print "Running"
        else:
            vm.append("OFF")  # POWER_STATE
        # print "OFF"
        if 'private' in parsed_json_response['servers'][i]['addresses']:
            ipv4 = parsed_json_response['servers'][i]['addresses']['private'][0]['addr']
            ipv6 = parsed_json_response['servers'][i]['addresses']['private'][1]['addr']
            vm.append("Private " + str(ipv4) + " " + str(ipv6))  # NETWORK
        # print "Private",ipv4," ",ipv6
        elif 'public' in parsed_json_response['servers'][i]['addresses']:
            ipv4 = parsed_json_response['servers'][i]['addresses']['public'][0]['addr']
            ipv6 = parsed_json_response['servers'][i]['addresses']['public'][1]['addr']
            vm.append("Private " + str(ipv4) + " " + str(ipv6))  # NETWORK
        # print "Public",ipv4," ",ipv6
        # print vm
        vmlist.append(vm)
    # print "======================================================================="

    print vmlist
    return vmlist


def getProjectID(ip):
    """"Get project id of the project demo"""
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
    parsed_json_response = json.loads(response.text)
    # print parsed_json_response
    gg = parsed_json_response['tenants']
    for ll in gg:
        if ll['name'] == 'demo':
            # print ll['id']
            return ll['id']


def main(ip, username, password):
    return list_vms(ip, username, password)
