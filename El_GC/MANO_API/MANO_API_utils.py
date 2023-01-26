import requests

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{"image":"vnf:monitoring", "network":"(id=input,ip=10.0.0.20/24)"}'
# response = requests.put('http://127.0.0.1:5001/restapi/compute/dc1/vnf_moni', headers=headers, data=data)

BASE_URL = 'http://127.0.0.1:5001/restapi/'


def deploy_vnf(
        vnf_name: str,
        vnf_img_name: str,
        vnf_ip_output: str,
        vnf_ip_input: str = '10.0.0.42/24',
        datacenter_name: str = 'dc1'):
    headers = {
        'Content-Type': 'application/json',
    }

    # 'network' = vnf's eth interfaces
    my_nw = f'(id=input,ip={vnf_ip_input})'
    if vnf_ip_output:
        my_nw += f',(id=output,ip={vnf_ip_output})'

    # Construct payload
    json_data = {
        'image': vnf_img_name,
        'network': my_nw,
    }

    my_url = BASE_URL + 'compute/' + datacenter_name + '/' + vnf_name
    # Send PUT request to vim-emu to deploy vnf
    r = requests.put(my_url, headers=headers, json=json_data)
    return r.json()


def test_vnf_deployment(
        vnf_name: str,
        datacenter_name: str = 'dc1') -> bool:
    headers = {
        'Content-Type': 'application/json',
    }
    my_url = BASE_URL + 'compute/' + datacenter_name + '/' + vnf_name
    r = requests.get(my_url, headers=headers)
    vnf_is_deployed = r.json().get('state').get('Running')
    return vnf_is_deployed
