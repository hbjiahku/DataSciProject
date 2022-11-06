import json
import os

NETWORK_CFG = "network_config"
DATA_SRC_CFG = "data_source_config"
SQL_SOURCE = "sqlite3"  # can be sqlite3 (local db file), or mysql (remote database server)


def get_config(config_name):
    with open(f"{os.path.dirname(__file__)}//{config_name}.json", "r") as f:
        cfg = json.load(f)
    return cfg
