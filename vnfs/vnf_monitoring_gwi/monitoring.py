import collections

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests

app = Flask(__name__)

GWI_IP = '10.0.0.2'
GWI_PORT = '8181'
GWI_URL = 'http://' + GWI_IP + ':' + GWI_PORT

MAX_LEN_STATES_DEQUE = 15
MAX_LEN_PING_DEQUE = 15
COLLECT_STATES_FREQ_S = 2
COLLECT_PING_FREQ_S = 2
STATE_REQ_TIMEOUT = 1
PING_REQ_TIMEOUT = 1

states = collections.deque([], maxlen=MAX_LEN_STATES_DEQUE)
pings = collections.deque([], maxlen=MAX_LEN_PING_DEQUE)


@app.route("/states", defaults={'list_len': MAX_LEN_STATES_DEQUE})
@app.route("/states/<int:list_len>")
def provide_state(list_len: int):
    # Avoid out of bounds
    if list_len > MAX_LEN_STATES_DEQUE:
        list_len = MAX_LEN_STATES_DEQUE
    # Return the list_len last elements of the list
    return list(states)[-list_len:]


@app.route("/pings", defaults={'list_len': MAX_LEN_STATES_DEQUE})
@app.route("/pings/<int:list_len>")
def provide_ping(list_len: int):
    # Avoid out of bounds
    if list_len > MAX_LEN_PING_DEQUE:
        list_len = MAX_LEN_PING_DEQUE
    # Return the list_len last elements of the list
    return list(pings)[-list_len:]


@app.route("/all")
def provide_all():
    return {'pings': list(pings), 'states': list(states)}


def collect_state():
    # Add timestamp to dict containing response
    state = {'state_req_send_timestamp': time.time()}
    try:
        r = requests.get(GWI_URL + '/health', timeout=STATE_REQ_TIMEOUT)
        state.update(r.json())
        state.update({'state_req_elapsed_time_s': r.elapsed.total_seconds()})
    except requests.exceptions.Timeout:
        state.update({'error': f'timeout after {STATE_REQ_TIMEOUT}s'})
    except requests.exceptions.TooManyRedirects:
        state.update({'error': 'badURL'})
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    states.append(state)

    print(f'Health request gave state: {state}')
    print(f'STATES: {states}')


def collect_ping():
    ping = {'req_send_timestamp': time.time()}
    try:
        r = requests.get(GWI_URL + '/ping', timeout=PING_REQ_TIMEOUT)
        ping.update(r.json())
        ping.update({'ping_req_elapsed_time_s': r.elapsed.total_seconds()})
    except requests.exceptions.Timeout:
        ping.update({'error': f'timeout after {PING_REQ_TIMEOUT}s'})
    except requests.exceptions.TooManyRedirects:
        ping.update({'error': 'badURL'})
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    print(f'Ping request gave ping: {ping}')

    pings.append(ping)
    print(f'Pings: {pings}')


scheduler = BackgroundScheduler()
collect_state_job = scheduler.add_job(collect_state, 'interval', seconds=COLLECT_STATES_FREQ_S)
collect_ping_job = scheduler.add_job(collect_ping, 'interval', seconds=COLLECT_PING_FREQ_S)

scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
