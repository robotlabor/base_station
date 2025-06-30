import time
import os
import subprocess
import json
from threading import Thread
from serial import Serial
from pyubx2 import UBXReader, UBXMessage, UBX_PROTOCOL
import f9p_basestation
import lgpio
from utm import from_latlon
from flask import Flask, Response

# GNSS Config
SURVEY_DURATION = 180  # seconds
ACC_LIMIT = 2000  # accuracy in mm
USB_PORT = '/dev/ttyGNSS'
USB_BAUD = 115200

# LED GPIO
LED_RED = 13
LED_GREEN = 12
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, LED_RED)
lgpio.gpio_claim_output(h, LED_GREEN)
lgpio.tx_pwm(h, LED_RED, 1000, 100)

# Serial Port Access 
subprocess.run(f"sudo chmod a+rw {USB_PORT}", shell=True)

# GNSS Setup 
f9p_basestation.settings(port=USB_PORT, baud=USB_BAUD, limit=ACC_LIMIT, duration=SURVEY_DURATION)
print("GNSS settings OK")
time.sleep(1.0)

# Reboot GNSS 
reboot = Serial(USB_PORT, USB_BAUD, timeout=5)
msg = UBXMessage("CFG", "CFG-RST", msgmode=1, navBbrMask=0, resetMode=4)
reboot.write(msg.serialize())
reboot.close()
print("GNSS reboot")
time.sleep(3.0)
subprocess.run(f"sudo chmod a+rw {USB_PORT}", shell=True)

# Wait for Survey-In
stream = Serial(USB_PORT, USB_BAUD, timeout=5)
br = UBXReader(stream, protfilter=UBX_PROTOCOL)
valid = False

try:
    for raw, parsed in br:
        if parsed and parsed.identity == "NAV-SVIN":
            print(f"SVIN duration: {parsed.dur} ({parsed.dur/SURVEY_DURATION*100:.1f}%), ACC_LIMIT: {ACC_LIMIT}, ACC: {parsed.meanAcc}, valid: {parsed.valid}, active: {parsed.active}")
            if parsed.active == 0:
                valid = parsed.valid
                break

    if valid:
        print("Survey-In ready,")
        #stream.close()
    else:
        print(" Survey-In faild.")
        lgpio.tx_pwm(h, LED_RED, 1000, 20)
        lgpio.tx_pwm(h, LED_GREEN, 1000, 80)
        stream.close()
        exit(1)

except Exception as e:
    print(f"Error: {e}")
    stream.close()
    lgpio.gpiochip_close(h)
    exit(1)

# Flask RTCM server
app = Flask(__name__)

@app.route('/rtcm')
def stream_rtcm():
    def generate():
        with Serial(USB_PORT, USB_BAUD, timeout=1) as ser:
            while True:
                chunk = ser.read(1024)
                if chunk:
                    yield chunk
    return Response(generate(), mimetype='application/octet-stream')

def run_http():
    print("RTCM szerver on: http://0.0.0.0:8000/rtcm")
    app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    http_thread = Thread(target=run_http, daemon=True)
    http_thread.start()

    try:
        while True:
            lgpio.tx_pwm(h, LED_RED, 1000, 0)
            lgpio.tx_pwm(h, LED_GREEN, 1000, 100) # Green
            time.sleep(1.0)  
    except KeyboardInterrupt:
        print("Stop...")
    finally:
        lgpio.tx_pwm(h, LED_RED, 1000, 0)
        lgpio.tx_pwm(h, LED_GREEN, 1000, 0)
        lgpio.gpio_write(h, LED_RED, 0)
        lgpio.gpio_write(h, LED_GREEN, 0)
        lgpio.gpiochip_close(h)

