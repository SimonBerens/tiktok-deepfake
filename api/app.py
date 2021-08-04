import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/queue_video", methods=["POST"])
def queue_video():
    video_idx = request.json["video_idx"]
    socketio.emit("video_queued", {"video_idx": video_idx, "time": time.time_ns()})
    return "success"


@app.route("/api/rawtext", methods=["GET", "POST"])
def handle_raw_text():
    body = request.get_json(force=True)
    raw_text = body.get("rawText")
    if not raw_text:
        raise BadRequest("Expected a rawText field in JSON body")
    print(f"Got raw text: {raw_text}")
    resp = jsonify(success=True)
    return resp


if __name__ == "__main__":
    socketio.run(app)
