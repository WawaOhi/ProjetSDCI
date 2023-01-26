from datetime import datetime
import requests
import os
import statistics

from apscheduler.schedulers.blocking import BlockingScheduler

from MANO_API.MANO_API_utils import deploy_vnf, test_vnf_deployment, delete_vnf
from SDNctrl_API.SDNctrl_API_utils import redirect_traffic, undo_redirect_traffic


def check_gi_ping(vnf_monitoring_IP_port: str = 'localhost:5000', req_timeout: int = 1) -> float:
    try:
        r = requests.get(vnf_monitoring_IP_port + '/pings/10', timeout=req_timeout)
        elapsed_times = []
        for ping in list(r.json()):
            time = ping.get('ping_req_elapsed_time_s', default=1)
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


def check_gi_states(vnf_monitoring_IP_port: str = 'localhost:5000', req_timeout: int = 1) -> float:
    try:
        r = requests.get(vnf_monitoring_IP_port + '/states/10', timeout=req_timeout)
        avg_loads = []
        for state in list(r.json()):
            avg_load = state.get('avgLoad', default=1)
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
    # TODO add counter to avoid infinite loops
    while not vnf_is_deployed:
        deploy_vnf(vnf_name='vnf_adapt', vnf_img_name='vnf:adaptation', vnf_ip_output='10.0.0.21/24')
        vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_adapt')
    redirect_traffic()


def shutdown_vnf_adapt():
    vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_adapt')
    # TODO add counter to avoid infinite loops
    while vnf_is_deployed:
        delete_vnf(vnf_name='vnf_adapt')
        vnf_is_deployed = test_vnf_deployment(vnf_name='vnf_adapt')
    undo_redirect_traffic()


def main_monitor_adapt(avg_load_threshold: float = 0.9, avg_elapsed_time_threshold: float = 1):
    print('We are in main_monitor! The time is: %s' % datetime.now())
    avg_elapsed_time = check_gi_ping()
    avg_load = check_gi_states()
    if (avg_elapsed_time > avg_elapsed_time_threshold) or (avg_load_threshold > avg_load_threshold):
        deploy_vnf_adapt()
    else:
        shutdown_vnf_adapt()
    # TODO shutdown vnf if going back to normal
    print(f'')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # Main monitor runs every 3 seconds
    scheduler.add_job(main_monitor_adapt(), 'interval', seconds=3)
    print('Welcome ! This is our wonderful General Controller. He monitors (almost) everything !')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
