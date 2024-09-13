import random
import os
from flask import Flask

ERROR_RATE = os.environ.get('ERROR_RATE', '90')

app = Flask(__name__)

def isError(percentage):
	return random.randint(1, 100) <= percentage

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/probe')
def probe():
	return "OK"

@app.route('/error')
def error():
	if isError(ERROR_RATE):
		return "Error found!", 500
	else:
		return "No error found!"

if __name__ == '__main__':
	print(f"Error rate is {ERROR_RATE}%")
	app.run(host='0.0.0.0', port=8080)
