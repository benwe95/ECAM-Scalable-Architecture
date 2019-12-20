from flask import Flask, request, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
import functions, requests, threading, logging, time

app = Flask(__name__)
FlaskJSON(app)

@app.route('/home')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['POST'])
def home():
    data = request.get_json()
    #logging.info("Request received: {}".format(data))
    command = data['command']
    res = {}

    if(command=='ping'):
        res = functions.ping_pong()
    elif(command=='sample'):
        res = functions.sample(data['size'], data['begin'], data['end'])
    elif(command=='sort'):
        res = functions.sort(data)

    logging.info("Response: {}".format(res))
    print(jsonify(res))
    return jsonify(res)

@app.route('/connect')
def connect():
    data = {"command": "connect",
            "name": "Benoît Wéry",
            "port": 5000}
    logging.info('ENTERED connect')
    return requests.post('http://172.17.3.35:8000', json=data)

if __name__=='__main__':
    #app.run(host='0.0.0.0', port=80)
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
    datefmt="%H:%H:%S")
    logging.info("Main    : before creating thread")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)


        #th = threading.Thread(target=functions.sort, args=(data,))
        #logging.info("Sort  : before running thread")
        #th.start()
        #logging.info("Sort  : wait for the thread to finish")
        #logging.info("Sort  : all done")
        #res = functions.sort(data)