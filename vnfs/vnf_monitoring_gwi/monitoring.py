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
COLLECT_STATES_FREQ_S = 1
COLLECT_PING_FREQ_S = 15
STATE_REQ_TIMEOUT = 0.5
PING_REQ_TIMEOUT = 0.5

states = collections.deque([], maxlen=MAX_LEN_STATES_DEQUE)
pings = collections.deque([], maxlen=MAX_LEN_PING_DEQUE)


@app.route("/state", defaults={'list_len': MAX_LEN_STATES_DEQUE})
@app.route("/state/<int:list_len>")
def provide_state(list_len: int):
    # Avoid out of bounds
    if list_len > MAX_LEN_STATES_DEQUE:
        list_len = MAX_LEN_STATES_DEQUE
    # Return the list_len last elements of the list
    return list(states)[-list_len:]


@app.route("/ping", defaults={'list_len': MAX_LEN_STATES_DEQUE})
@app.route("/ping/<int:list_len>")
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
    try:
        r = requests.get(GWI_URL + '/health', timeout=STATE_REQ_TIMEOUT)
        state = r.json()
    except requests.exceptions.Timeout:
        state = [{'error': 'timeout'}]
    except requests.exceptions.TooManyRedirects:
        state = [{'error': 'badURL'}]
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    state.append({'timestamp': time.time()})
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f'Health request at {current_time} gave state {state}')

    states.append(state)

    print(f'STATES: {list(states)}')


def collect_ping():
    try:
        r = requests.get(GWI_URL + '/ping', timeout=PING_REQ_TIMEOUT)
        ping = r.json()
    except requests.exceptions.Timeout:
        ping = [{'error': 'timeout'}]
    except requests.exceptions.TooManyRedirects:
        ping = [{'error': 'badURL'}]
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    ping.append({'timestamp': time.time()})

    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f'Ping request at {current_time} gave ping {ping}')

    pings.append(ping)
    print(f'Pings: {pings}')


scheduler = BackgroundScheduler()
collect_state_job = scheduler.add_job(collect_state, 'interval', seconds=COLLECT_STATES_FREQ_S)
collect_ping_job = scheduler.add_job(collect_ping, 'interval', seconds=COLLECT_PING_FREQ_S)

scheduler.start()

if __name__ == "__main__":
    app.run()
