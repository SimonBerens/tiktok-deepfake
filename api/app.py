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


before_filter = defaultdict(int)
after_filter = defaultdict(int)


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

    vid_type = int(response.fulfillment_text.split(' ')[-1])

    if time.time_ns() - after_filter[vid_type] < 60 * 10 ** 9:
        return ""
    after_filter[vid_type] = time.time_ns()

    queue_video(vid_type)

    return resp


if __name__ == "__main__":
    socketio.run(app)
