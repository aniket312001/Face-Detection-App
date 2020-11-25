from flask import Flask, Response, render_template, request
import cv2

app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face_video')
def face_video():
    return Response(detect(), mimetype='multipart/x-mixed-replace; boundary=frame')

def detect():
    cap = cv2.VideoCapture(0)  # Web Camera
    cascade = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')  #detecting cascade file

    while True:
        success,img = cap.read()  # video in img

        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # Gray

        cords = cascade.detectMultiScale(grayimg, 1.1, 3)  

        for x,y,w,h in cords:  
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 3)  # Rectangle

        img = cv2.imencode('.jpg', img)[1].tobytes() 

        try:
            data = request.args.get('btn')

            if data=='stop':
                cap.release()

        except:
            pass

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


@app.route('/stop')
def stop_video():
    return render_template('bye.html')   

if __name__ == "__main__":
    app.run(debug=True)

