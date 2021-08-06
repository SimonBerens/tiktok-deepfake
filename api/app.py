import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from werkzeug.exceptions import BadRequest
from google.protobuf.json_format import MessageToDict
from dialogflow import get_response
from collections import defaultdict
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/queue_video", methods=["POST"])
def queue_video(video_type=None):
    if not video_type:
        video_type = request.json["video_type"]
    socketio.emit("video_queued", {"video_type": video_type})
    return "success"


@app.route("/api/rawtext", methods=["GET", "POST"])
def handle_raw_text():
    body = request.get_json(force=True)
    raw_text = body.get("rawText")
    if not raw_text:
        raise BadRequest("Expected a rawText field in JSON body")
    print(f"Got raw text: {raw_text}")

    response = get_response(raw_text)
    resp = jsonify(MessageToDict(response))

    vid_type = int(response.fulfillment_text.split(' ')[-1])

    queue_video(vid_type)

    return resp


if __name__ == "__main__":
    socketio.run(app)
