from datetime import datetime
import requests
import os
import statistics

from apscheduler.schedulers.blocking import BlockingScheduler

from MANO_API.MANO_API_utils import deploy_vnf, test_vnf_deployment, delete_vnf
from SDNctrl_API.SDNctrl_API_utils import redirect_traffic, undo_redirect_traffic


def check_gi_ping(vnf_monitoring_IP_port: str = 'localhost:32806', req_timeout: int = 1) -> float:
    try:
        r = requests.get('http://' + vnf_monitoring_IP_port + '/pings/10', timeout=req_timeout)
        elapsed_times = []
        for ping in list(r.json()):
            time = ping.get('ping_req_elapsed_time_s', 1)
            elapsed_times.append(time)
        avg_elapsed_time = statistics.mean(elapsed_times)
        return avg_elapsed_time

    except requests.exceptions.Timeout:
        print(f'ERROR: timeout during gi ping monitoring after {req_timeout}s')
        print('You should check that vnf_monitoring works correctly !')
        return 100000
    except requests.exceptions.TooManyRedirects:
        print('ERROR badURL')
        print('You should check vnf_monitoring\'s IP')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def check_gi_states(vnf_monitoring_IP_port: str = 'localhost:32806', req_timeout: int = 1) -> float:
    try:
        r = requests.get('http://' + vnf_monitoring_IP_port + '/states/10', timeout=req_timeout)
        avg_loads = []
        for state in list(r.json()):
            avg_load = state.get('avgLoad', 1)
            avg_loads.append(avg_load)
        avg_avg_load = statistics.mean(avg_loads)
        return avg_avg_load

    except requests.exceptions.Timeout:
        print(f'ERROR: timeout during gi state monitoring after {req_timeout}s')
        print('You should check that vnf_monitoring works correctly !')
        return 1
    except requests.exceptions.TooManyRedirects:
        print('ERROR badURL')
        print('You should check vnf_monitoring\'s IP')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def deploy_vnf_adapt():
    vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_adapt')
    max_tries = 5
    counter = 0
    while (not vnf_is_deployed) and (counter < max_tries):
        counter += 1
        deploy_vnf(vnf_name='vnf_adapt', vnf_img_name='vnf:adaptation', vnf_ip_output='10.0.0.21/24')
        vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_adapt')
        if vnf_is_deployed:
            print('VNF successfully deployed !')
            redirect_traffic()
        else:
            print('Error while deploying vnf :(')


def shutdown_vnf_adapt():
    vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_adapt')
    max_tries = 5
    counter = 0
    while vnf_is_deployed and (counter < max_tries):
        delete_vnf(vnf_name='vnf_adapt')
        vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_adapt')
        if vnf_is_deployed:
            print('Error while shutting down vnf :(')
            undo_redirect_traffic()
        else:
            print('VNF was successfully shut down !')


def deploy_vnf_monitoring():
    vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_moni')
    max_tries = 5
    counter = 0
    while (not vnf_is_deployed) and (counter < max_tries):
        counter += 1
        deploy_vnf(vnf_name='vnf_moni', vnf_img_name='vnf:monitoring', vnf_ip_output='10.0.0.20/24')
        vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_moni')
        if vnf_is_deployed:
            print('VNF successfully deployed !')
            redirect_traffic()
        else:
            print('Error while deploying vnf :(')


def main_monitor_adapt(avg_load_threshold: float = 0.9, avg_elapsed_time_threshold: float = 1):
    print('We are in main_monitor! The time is: %s' % datetime.now())
    avg_elapsed_time = check_gi_ping()
    avg_load = check_gi_states()
    print(
        f'The average response time of the GI (10 last seconds) is {avg_elapsed_time} (threshold : {avg_elapsed_time_threshold})')
    print(f'The average of average loads of the GI (10 last seconds) is {avg_load} (threshold : {avg_load_threshold})')
    if (avg_elapsed_time > avg_elapsed_time_threshold) or (avg_load > avg_load_threshold):
        print('One of the threshold is exceeded ! Deploying vnf...')
        deploy_vnf_adapt()

    else:
        print('Everything is ok ! GC will ensure that vnf is down...')
        shutdown_vnf_adapt()


if __name__ == '__main__':
    print('Welcome ! This is our wonderful General Controller. He monitors (almost) everything !')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    print('Deploying monitoring VNF...')
    deploy_vnf_monitoring()

    scheduler = BlockingScheduler()
    # Main monitor runs every 3 seconds
    scheduler.add_job(main_monitor_adapt(), 'interval', seconds=3)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
