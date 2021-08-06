import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from werkzeug.exceptions import BadRequest
from google.protobuf.json_format import MessageToDict
from dialogflow import get_response
from collections import defaultdict
from video_config import NUM_VIDEOS
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/queue_video", methods=["POST"])
def queue_video(video_type=None):
    if not video_type:
        video_type = request.json["video_type"]
    socketio.emit("video_queued",
                  {
                      "video_type": video_type,
                      "video_idx": random.randint(0, NUM_VIDEOS[video_type] - 1)
                  })
    return "success"


before_filter = defaultdict(lambda: time.time_ns())
after_filter = defaultdict(lambda: time.time_ns())


@app.route("/api/rawtext", methods=["GET", "POST"])
def handle_raw_text():
    body = request.get_json(force=True)
    raw_text = body.get("rawText")
    if not raw_text:
        raise BadRequest("Expected a rawText field in JSON body")
    print(f"Got raw text: {raw_text}")

    if time.time_ns() - before_filter[raw_text] < 60 * 10 ** 9:
        return ""
    before_filter[raw_text] = time.time_ns()

    response = get_response(raw_text)
    resp = jsonify(MessageToDict(response))

    if time.time_ns() - after_filter[resp] < 60 * 10 ** 9:
        return ""
    after_filter[resp] = time.time_ns()

    # TODO: call queue_video with the video ID from response
    return resp


if __name__ == "__main__":
    socketio.run(app)
