from camera import VideoCamera
from flask import Flask, render_template, request, jsonify, Response
import requests
import base64,cv2

flag = False
app=Flask(__name__)
def gen():
    flag = True
    obj = VideoCamera()
    while flag:
        data= obj.get_frame()

        frame=data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    print(flag)
    del obj

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen2():
    flag = False
@app.route('/video_close')
def video_close():
    return Response(gen2())

if __name__=="__main__":
    app.run(debug=True)#,host="192.168.43.161")
