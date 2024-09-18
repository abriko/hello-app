import random
import os
import signal
import time
from flask import Flask

ERROR_RATE = int(os.environ.get('ERROR_RATE', '90'))
PROBE_OK = True

app = Flask(__name__)

def isError(percentage):
	return random.randint(1, 100) <= percentage

def factorial(n):
  if n == 0:
    return 1
  else:
    return n * factorial(n - 1)

def increase_cpu_usage(duration):
  start_time = time.time()
  while time.time() - start_time < duration:
    result = factorial(900)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/probe')
def probe():
	if PROBE_OK:
		return "OK"
	else:
		time.sleep(60)
		return "Backend service unreachable!", 503

@app.route('/probe_switch')
def probeSwitch():
	global PROBE_OK
	PROBE_OK = not PROBE_OK
	return "Changed"

@app.route('/error')
def error():
	if isError(ERROR_RATE):
		return "Error found!", 500
	else:
		return "No error found!"

@app.route('/error_crash')
def errorCrash():
	os.kill(os.getpid(), signal.SIGINT)
	raise RuntimeError('System failure!')

@app.route('/heavy_load')
def heavyLoad():
	increase_cpu_usage(3)
	return "All good, calculate done!"

if __name__ == '__main__':
	print(f"⚠️ Error rate is {ERROR_RATE}%")
	app.run(host='0.0.0.0', port=8080)
