# -*- coding: utf-8 -*-
import argparse
import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from application import create_app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MV')
    parser.add_argument('--port', action="store", dest="port", type=int, default=5000)
    args = parser.parse_args()
    host = '0.0.0.0'
    port = args.port
    app.logger.info("listen on %s:%s" % (host, port))
    app.run(host=host, port=port)
