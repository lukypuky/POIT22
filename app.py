from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect  
import time
import serial
import MySQLdb 
import configparser as ConfigParser

async_mode = None

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate=9600

def background_thread(args):
    count = 0
    dataList = []
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb) 
    while True:
        read_ser = ser.readline().decode()

        values = read_ser.split(",")
        humidity = float(values[0])
        temperature = float(values[1])
        
        if args:
            A = dict(args).get('A')
            btnV = dict(args).get('btn_value')
        else:
            A = 1
            btnV = 'null'
            
        btnV = dict(args).get('btn_value') 
        socketio.sleep(2)
        
        if btnV == 'start':
            print("ide")
            count += 1
            dataDict = {
                "x": count,
                "y": humidity,
                "t": temperature}
            dataList.append(dataDict)
            
#             print(humidity)
#             print(temperature)
                    
            socketio.emit('my_response',
                {'data': humidity, 'temp': temperature, 'count': count},
                namespace='/test') 
        elif btnV == 'stop':
            print("neide")
            if len(dataList)>0:
#                 print(dataList)
                strDataList = str(dataList).replace("'", "\"")
                cursor = db.cursor()
                query = "INSERT INTO senzor (meranie) VALUES ('%s')" % (strDataList)
                cursor.execute(query)
                db.commit()
             
                fo = open("static/data.txt","a+")
                fo.write("%s\r\n" %strDataList)
                fo.close()
          
                dataList = []    
    db.close()

@app.route('/')
def hello():
    return render_template('indexz.html')

@app.route('/indexz', methods=['GET', 'POST'])
def graphlive():
    return render_template('indexz.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['A'] = message['value']    
 
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'temp': 'Disconnected!', 'count': session['receive_count']})
    disconnect()
    
@app.route('/dbdata/<string:num>', methods=['GET', 'POST'])
def dbdata(num):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute("SELECT meranie FROM senzor WHERE id=%s", num)
  rv = cursor.fetchone()
  return str(rv[0])

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())

@socketio.on('click_eventStart', namespace='/test')
def db_message(message):   
    session['btn_value'] = 'start'

@socketio.on('click_eventStop', namespace='/test')
def db_message(message):   
    session['btn_value'] = 'stop'

@socketio.on('slider_event', namespace='/test')
def slider_message(message):   
    session['slider_value'] = message['value']  

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)
    
@app.route('/read/<string:num>', methods=['GET', 'POST'])
def readmyfile(num):
    fo = open("static/data.txt","r")
    rows = fo.readlines()
    return rows[int(num)]

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
