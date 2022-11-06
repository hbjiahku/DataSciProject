import json
import threading
from flask import Flask, Blueprint, request, jsonify
import pandas as pd

from config.config_helper import get_config, NETWORK_CFG
from interface.interface import load_interface

interface = load_interface(debug_file=False, server_side=True)


def get_bp():
    bp = Blueprint("trading server", __name__)

    @bp.route("/print", methods=["POST"])
    def rest_print():
        print("Hello")
        return jsonify({"result": None})

    @bp.route("/dispatch", methods=["POST"])
    def rest_dispatch():
        input_d = request.get_json(cache=False)
        d = input_d["request"]
        if isinstance(d["args"], dict):
            res = interface[d["fname"]](**d["args"])
        elif isinstance(d["args"], list):
            res = interface[d["fname"]](d["args"])
        else:
            res = None
        res_json = {}
        if isinstance(res, pd.DataFrame):
            res_json["value"] = res.to_json()
            res_json["type"] = "pandas.DataFrame"
        else:
            res_json["value"] = json.dumps(res)

        return jsonify({"result": res_json})

    return bp


class RestListener(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        app = Flask("trading_server")
        _bp = get_bp()
        app.register_blueprint(_bp, url_prefix="/api/v1")
        app.run(host=self.host, port=self.port, threaded=True)


if __name__ == "__main__":
    network_config = get_config(NETWORK_CFG)
    REST_THREAD = RestListener(host=network_config["host"], port=network_config["port"])
    REST_THREAD.run()
