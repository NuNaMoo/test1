from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import RPi.GPIO as GPIO

app = Flask(__name__)

##########   variables  ##########
state = 'ready'
address = 'empty'

##########  functions  ###########
def AED_state(state):
	if state == 'ready':
		GPIO.output(21, 1)
		print('***********')
                print('*Code Blue*')
                print('***********')

        elif state == 'alraming':
                GPIO.output(21, 0)
                print('*********')
                print('*Nothing*')
                print('*********')

	elif state == 'arrived':
		GPIO.output(21, 0)
		print('*************')
		print('*AED Arrived*')
		print('*************')

def reset_variables():
	global state
	global adrress
	state = 'ready'
	address = 'empty'

##########  routes & view functions  ##########
@app.route('/') #director
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		global state
		if state=='ready':
			return render_template('script.html', state=state,address=address)
		else:
			return render_template('script2.html', state=state,address=address)

@app.route('/login', methods=['POST']) 	#login
def do_admin_login():
        if request.form['password']=='1q2w3e4r' and request.form['username']=='admin':
                session['logged_in'] = True
		return home()
        else:
                flash('Invalid credential')
	return home()

@app.route('/logout')    #logout
def logout():
	session['logged_in'] = False
	reset_variables()

	return home()

@app.route('/control', methods=['POST']) 	#send address into AED
def AED_control():
	global state
	global address
	address = request.form['address']

	state='alraming'
	AED_state(state)

	print 'adrress is'
	print address

	return home()

@app.route('/control')
def renew():
	return home()

############################################################################

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
AED_state('ready')

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=10001)
	GPIO.cleanup()
