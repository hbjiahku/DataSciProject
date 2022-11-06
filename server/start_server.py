from server.flask_api import get_config, NETWORK_CFG, RestListener

network_config = get_config(NETWORK_CFG)
REST_THREAD = RestListener(host=network_config["host"], port=network_config["port"])
REST_THREAD.run()
