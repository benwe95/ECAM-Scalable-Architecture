from flask import Flask, request, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
import functions

app = Flask(__name__)
FlaskJSON(app)

@app.route('/home')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['POST'])
def home():
    data = request.get_json()
    print("Request: {}".format(data))
    command = data['command']
    res = {}

    if(command=='ping'):
        res = functions.ping_pong()
    elif(command=='sample'):
        res = functions.sample(data['size'], data['begin'], data['end']),
    elif(command=='sort'):
        res = functions.sort(data)

    print("Response: {}".format(res))
    return jsonify(res)

if __name__=='__main__':
    #app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=5000, debug=True)


