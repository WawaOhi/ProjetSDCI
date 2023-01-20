import collections

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import time

app = Flask(__name__)

GWI_IP = '127.0.0.1'

MAX_LEN_STATES_DEQUE = 15
MAX_LEN_PING_DEQUE = 15
COLLECT_STATES_FREQ_S = 1
COLLECT_PING_FREQ_S = 15

states = collections.deque([], maxlen=MAX_LEN_STATES_DEQUE)
pings = collections.deque([], maxlen=MAX_LEN_PING_DEQUE)

# @app.route("/state")
# def provide_state():
#     return list(states)


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
    return 'PING'


def collect_state():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    # print(f'Health request at {current_time}')
    states.append(f'HEALTH at {current_time}')
    print(f'STATES: {states}')


def collect_ping():
    # print(f'Ping request at {time.strftime("%H:%M:%S", time.localtime())}')
    print()


scheduler = BackgroundScheduler()
collect_state_job = scheduler.add_job(collect_state, 'interval', seconds=COLLECT_STATES_FREQ_S)
collect_ping_job = scheduler.add_job(collect_ping, 'interval', seconds=COLLECT_PING_FREQ_S)

scheduler.start()

if __name__ == "__main__":
    app.run()
