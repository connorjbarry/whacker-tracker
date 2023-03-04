import eventlet
import socketio
import threading

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'},
})

METRICS = {
    'club_speed': 1,
    'club_angle': 1,
    'ball_speed': 1,
    'ball_distance': 1,
    'smash_factor': 1,
    'launch_angle': 1,
}


@sio.event
def metrics(sid, data):
    threading.Timer(10.0, metrics, [sid, data]).start()
    print("metrics sending...")
    METRICS['club_speed'] += 1
    METRICS['club_angle'] += 1
    METRICS['ball_speed'] = 2
    METRICS['ball_distance'] = 2
    METRICS['smash_factor'] = 2
    METRICS['launch_angle'] = 2
    metric_send(sid, data)


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.start_background_task(metrics, sid, 'data')


@sio.on('metrics')
def metric_send(sid, data):
    print('message emmited... ', sid)
    sio.emit('metrics', {
        'club_speed': METRICS['club_speed'],
        'club_angle': METRICS['club_angle'],
        'ball_speed': METRICS['ball_speed'],
        'ball_distance': METRICS['ball_distance'],
        'smash_factor': METRICS['smash_factor'],
        'launch_angle': METRICS['launch_angle'],
    })


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.on('end')
def end(sid, data):
    print('end ', sid)


@sio.on('start')
def start(sid, data):
    print('start ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
