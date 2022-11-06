import pandas as pd
import requests
import json
import datetime

from config.config_helper import get_config, NETWORK_CFG
from time_helper import xltoday, xl_to_date, add_period, date_to_xl


class RestMeta:
    def __init__(self, protocol=None, host=None, port=None, api_path=None):
        self.host = host
        self.port = port
        self.api_path = api_path
        self.url = "{}://{}:{}{}".format(protocol, host, port, api_path)

    def post(self, fname, data={}):
        response = requests.post(
            self.url + fname, json=data
        )
        return response.json()

    def get(self, fname):
        response = requests.get(
            self.url + fname
        )
        return response.json()


class RestProxy(RestMeta):
    def get_api_list(self):
        pass

    def get_interface(self):
        pass

    def dispatch(self, request):
        return self.post("/dispatch", data=request)


def create_request(fname, arg_d):
    '''

    :param fname: str function name
    :param arg_d: arguments dictionary {argn:argv}
    :return: dict
    '''

    def conv_parameter(param):
        if isinstance(param, (list, tuple)):
            conv_p = [conv_parameter(p) for p in param]
        elif isinstance(param, datetime.datetime) or isinstance(param, datetime.date):
            conv_p = date_to_xl(param)
        else:
            conv_p = param
        return conv_p

    rd = {}
    rd["fname"] = fname
    rd["args"] = {}
    for argn in arg_d:
        rd["args"][argn] = conv_parameter(arg_d[argn])
    return rd


def format_output(res):
    res = res.get('result', "Err")
    if res == "Err":
        return "Err"
    elif res == "null":
        return None
    else:
        res_v = json.loads(res["value"])
        res_t = res.get("type", None)
    if res_t == "pandas.DataFrame":
        return pd.DataFrame(res_v)
    else:
        return res_v


def funct_call(fname, **kwargs):
    rd = create_request(fname, kwargs)
    network_config = get_config(NETWORK_CFG)
    s = RestProxy(network_config["protocol"], network_config["host"],
                  network_config["port"], network_config["api_path"])
    response = s.dispatch({"request": rd})
    result = format_output(response)

    return result
