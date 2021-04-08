from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response
import requests
import base64,cv2


app=Flask(__name__, static_folder="./build", static_url_path='/')
def gen(camera):
    while True:
        data= camera.get_frame()

        frame=data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return app.send_static_file('index.html')
# def home_page():
#     return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_close')
def video_close():
    VideoCcamera.__del__

if __name__=="__main__":
    app.run(debug=True)#,host="192.168.43.161")


# cd api/venv/Scripts && flask.exe run --no-debugger