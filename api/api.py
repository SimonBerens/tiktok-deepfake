from flask import Flask, request
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/queue_video', methods=["POST"])
def queue_video():
    video_idx = request.json['video_idx']
    socketio.emit('video_queued', {'video_idx': video_idx, 'time': time.time_ns()})
    return "success"


if __name__ == '__main__':
    socketio.run(app)
