from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO
import time

from picamera2 import Picamera2
import cv2

#NOTE:  /video_feed creates a path that is used in the cam.html template
#       invoked with <img src="{{ url_for('video_feed') }}" class="img-fluid" alt="Video Feed">

camera = Picamera2()

camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

app = Flask(__name__)

def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



# Set up GPIO for motor control
motor_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)
pwm = GPIO.PWM(motor_pin, 1000)
pwm.start(0)

@app.route('/')
def index():
    return render_template('piui.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    angle = data['angle']
    force = data['force']

#    # Convert joystick data to PWM duty cycle
    duty_cycle = (force / 100) * 100  # Normalize force to PWM duty cycle
#
    # Apply PWM to control motor speed
    pwm.ChangeDutyCycle(duty_cycle)
#
    return 'OK'

@app.route('/stop', methods=['POST'])
def stop():
    # Stop the motor when the joystick is released
    pwm.ChangeDutyCycle(0)
    return 'OK'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
