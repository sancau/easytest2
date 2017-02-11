# -*- coding: utf-8 -*-

import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from temperature.required_input_info import REQUIRED_INPUT_INFO
from temperature.temperature_mode_handler import TemperatureModeHandler

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST', 'GET'])
def handle():
    if request.method == 'GET':
        return jsonify(REQUIRED_INPUT_INFO)
    try:
        payload = request.get_json(force=True)
        handler = TemperatureModeHandler()
        result = handler.handle(payload)
        if not result:
            print(payload)
            return jsonify(error='Invalid input data provided.'), 400
        return json.dumps(result)
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run()
