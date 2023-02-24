import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'},
})


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.on('connect')
def my_message(sid, data):
    sio.emit('my response', {
        'club_speed': 96,
        'club_angle': 8,
        'ball_speed': 105,
        'ball_distance': 250,
        'smash_factor': 1,
        'launch_angle': 40,
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
