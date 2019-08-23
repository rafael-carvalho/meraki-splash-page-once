import traceback
import os
import meraki

# SET THIS UP
API_KEY = None
ORG_NAME = None #'Rafael Carvalho' + 'aaa'
NET_NAME = None #'San Francisco' + 'aaa'
SSID_NAME = None #'SplashSSID' + 'aaa'

#If you have this information handy, you can pre-fill the items below. If not, the script will find it for you.
ORG_ID = ''
NETWORK_ID = ''
SSID_ID = None


def get_org_id(api_key, org_name):
    orgs = meraki.myorgaccess(api_key, suppressprint=True)
    id = [x['id'] for x in orgs if x['name'] == org_name]
    if id:
        id = id[0]
    else:
        raise Exception('Org with name {} could not be found'.format(org_name))
    return id


def get_network_id(api_key, org_id, network_name):
    networks = meraki.getnetworklist(api_key, org_id, suppressprint=True)
    id = [x['id'] for x in networks if x['name'] == network_name]
    if id:
        id = id[0]
    else:
        raise Exception('Network with name {} could not be found'.format(network_name))
    return id


def get_ssid_id(api_key, network_id, ssid_name):
    ssids = meraki.getssids(api_key, network_id, suppressprint=True)
    id = [x['number'] for x in ssids if x['name'] == ssid_name]
    if id:
        id = id[0]
    else:
        raise Exception('SSID with name {} could not be found'.format(ssid_name))
    return id


def get_clients(api_key, network_id, ssid_name, perPage=100, t0=None, timespan=None, startingAfter=None, endingBefore=None):
    clients = meraki.getallclients(api_key, network_id, suppressprint=True)
    #print(clients)
    clients = [x for x in clients if x['ssid'] == ssid_name]
    return clients


def update_splash_page_expiration_clients(api_key, ssid_id, clients_list, org_id, network_id, page_size=100):
    clients_macs = []
    # print(clients_list)
    #print(clients_macs)
    updated_list = list()
    for client in clients_macs:
        mac = client['mac']
        action = {
            "ssids": {
                f"{ssid_id}": {
                    "isAuthorized": True
                }
            }
        }
        result = meraki.updateclientsplash(api_key, network_id, mac, action)
        if not (result and 'ssid' in result):
            print(result)
            raise Exception('Error when updating policy for {}'.format(mac))
        else:
            updated_list.append(client)
            print('OK for {}'.format(mac))


    # Use action batch to create actual demo networks, cloning from base
    '''
    
    actions = list()
    for mac in clients_macs:
        action = {
                  "ssids": {
                    f"{ssid_id}": {
                      "isAuthorized": True
                    }
                  }
                }
        actions.append({
            'resource': f'/networks/{network_id}/clients/{mac}/splashAuthorizationStatus',
            'operation': 'update',
            'body': action
        })

    print(actions)
    out = create_action_batch(api_key, org_id, True, True, actions)
    print(out)
    '''

def raise_missing_param_exception(param):
    raise Exception(f'You need to provide {param}. You can hard code it or set it as an environment variable')

def check_params():
    api_key = os.getenv('API_KEY', API_KEY)
    org_name = os.getenv('ORG_NAME', ORG_NAME)
    net_name = os.getenv('NETWORK_NAME', NET_NAME)
    ssid_name = os.getenv('SSID_NAME', SSID_NAME)
    if api_key and org_name and net_name and ssid_name:
        return api_key, org_name, net_name, ssid_name
    else:
        if not api_key:
            raise_missing_param_exception('API_KEY')
        elif not org_name:
            raise_missing_param_exception('ORG_NAME')
        elif not net_name:
            raise_missing_param_exception('NETWORK_NAME')
        elif not ssid_name:
            raise_missing_param_exception('SSID_NAME')

def main_function(event=None, context=None):
    api_key, org_name, net_name, ssid_name = check_params()
    try:
        org_id = ORG_ID
        if not org_id:
            org_id = get_org_id(api_key, org_name)
            #print(org_id)

        net_id = NETWORK_ID
        if not net_id:
            net_id = get_network_id(api_key, org_id, net_name)
            #print(net_id)

        ssid_id = SSID_ID
        if not ssid_id:
            ssid_id = get_ssid_id(api_key, net_id, ssid_name)

        clients_list = get_clients(api_key, net_id, ssid_name)

        if clients_list:
            printable = [(x['mac'], x['description']) for x in clients_list]
            print(f'Updating policies for: {printable}')
            update_splash_page_expiration_clients(api_key, ssid_id, clients_list, org_id, net_id)
            print('Updated splash page expiration for {} clients on SSID {}'.format(len(clients_list), SSID_NAME))
        else:
            print('No clients to update on SSID {}'.format(SSID_NAME))
    except Exception as err:
        traceback.print_exc()

if __name__ == '__main__':
    main_function()
