import eventlet
import socketio
import logging
import coloredlogs
import asyncio
import discover_ble
from discover_ble import connected_to_peripheral
import Adafruit_BluefruitLE

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'},
})

ble = Adafruit_BluefruitLE.get_provider()


coloredlogs.install(fmt='%(asctime)s | %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level='INFO')

METRICS = {
    'club_speed': 1,
    'club_angle': 1,
    'ball_speed': 1,
    'ball_distance': 1,
    'smash_factor': 1,
    'launch_angle': 1,
}


@ sio.event
def metrics(sid, data):
    while(True):
        logging.info("updating metrics...")
        METRICS['club_speed'] += 1
        METRICS['club_angle'] += 1
        METRICS['ball_speed'] += 1
        METRICS['ball_distance'] += 1
        METRICS['smash_factor'] += 1
        METRICS['launch_angle'] += 1
        metric_send(sid, data)
        eventlet.sleep(8)


@ sio.event
def connect(sid, environ):
    logging.info(f'connect {sid}')
    # logging.error("starting background task...")
    sio.start_background_task(ble_connect, sid, 'data')
    # sio.start_background_task(metrics, sid, 'data')


@ sio.on('metrics')
def metric_send(sid, data):
    logging.info(f'metrics emitted... {sid}')
    sio.emit('metrics', {
        'club_speed': METRICS['club_speed'],
        'club_angle': METRICS['club_angle'],
        'ball_speed': METRICS['ball_speed'],
        'ball_distance': METRICS['ball_distance'],
        'smash_factor': METRICS['smash_factor'],
        'launch_angle': METRICS['launch_angle'],
    })


@ sio.event
def disconnect(sid):
    logging.error(f'disconnect {sid}')


@ sio.on('end')
def end(sid, data):
    # print('end ', sid)
    pass


@ sio.on('start')
def start(sid, data):
    # print('start ', sid)
    pass


@ sio.event
def ble_connect(sid, data):
    for _ in range(10):
        ble.initialize()
        print("ble initialized\n")
        ble.run_mainloop_with(discover_ble.search_ble)
        print("ble mainloop aborted\n")
        sio.start_background_task(metrics, sid, 'data')
        eventlet.sleep(25)
    # if connected_to_peripheral:


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
