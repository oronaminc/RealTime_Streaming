#!/usr/bin/python3


from datetime import datetime
from flask import Flask
from flask import render_template
from flask import Response
from flask import request
from cv2 import *

app = Flask(__name__)


@app.route("/")
def main():
    time_str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return render_template('main.html', time=time_str, visitor_ip=str(request.remote_addr))


def gen():
    cam = VideoCapture(0)
    encode_param = [int(IMWRITE_JPEG_QUALITY), 100]
    while True:
        cam_opened, img = cam.read()
        cv2.rectangle(img, (10,10), (100,100), (255,255,255), 5)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        ret, jpg_frame = imencode('.jpg', img, encode_param)
        frame = jpg_frame.tobytes() # jpg_frame is of type numpy.ndarray

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.debug = True
app.run(host = 'localhost', port=8080)

