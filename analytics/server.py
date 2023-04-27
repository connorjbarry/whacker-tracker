import eventlet
import socketio
import logging
import coloredlogs
from FileModificationHandler import FileModified
import algorithms
import pickle

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'},
})

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
def metrics(sid, data, club_speed, club_angle, ball_speed, ball_distance, smash_factor, launch_angle):

    logging.info("updating metrics...")
    METRICS['club_speed'] = club_speed
    METRICS['club_angle'] = club_angle
    METRICS['ball_speed'] = ball_speed
    METRICS['ball_distance'] = ball_distance
    METRICS['smash_factor'] = smash_factor
    METRICS['launch_angle'] = launch_angle
    metric_send(sid, data)


@ sio.event
def connect(sid, environ):
    logging.info(f'connect {sid}')
    # detect = FileModified('data.txt', detect_change(sid))

    # while True:
    #     print("starting file detection...")
    #     detect.start()
    # logging.error("starting background task...")
    # sio.start_background_task(ble_connect, sid, 'data')
    # ble_connect(sid, 'data')
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

# @ sio.event
# def ble_connect(sid, data):
#     pass
# #     ble.initialize()
# #     ble.run_mainloop_with(run_ble)
#     # metrics(sid, data)
#     # for _ in range(10):
#     #     ble.initialize()
#     #     print("ble initialized\n")
#     #     ble.run_mainloop_with(discover_ble.search_ble)
#     #     print("ble mainloop aborted\n")
#     #     sio.start_background_task(metrics, sid, 'data')
#     # eventlet.sleep(25)
#     # if connected_to_peripheral:


@sio.on("detection")
def file_detect(sid, data):
    print(data)
    detect = FileModified('data.txt', detect_change, sid)
    print("starting file detection...")
    detect.start()


def detect_change(sid):
    with open('data.txt', 'rb') as f:
        print("file change detected, calculating metrics...")
        sensor_data = pickle.load(f)
        print(sensor_data)
    fv, bs, bd, sf, cfa, la = algorithms.process_individal_sensor_data(
        sensor_data)

    fv = round(fv, 2)
    bs = round(bs, 2)
    bd = round(bd, 2)
    sf = round(sf, 2)
    cfa = round(cfa, 2)
    la = round(la, 2)

    print("metrics calculated, sending to client...")
    metrics(sid, 'data', fv, cfa, bs, bd, sf, la)

    return True


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
