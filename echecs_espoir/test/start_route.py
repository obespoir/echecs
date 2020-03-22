# coding=utf-8
"""
author = jamon
"""


if __name__ == "__main__":
    import sys
    sys.path.append("../")    # 添加项目的根目录到系统路径中

import logging

from obespoir.rpcserver import handler
from obespoir.share.ob_log import logger
from obespoir.share.parse_json import ParseJson
from obespoir.server.server import Server


if __name__ == "__main__":
    main_server = Server()
    serv_config = ParseJson.loads("../route_config.json")
    logger.init(module_name=serv_config.get("name"), log_dir=serv_config.get("log_dir", "../logs/")
                , level=serv_config.get("log_level", logging.DEBUG))
    main_server.start(serv_config)

