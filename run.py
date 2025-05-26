#!/usr/bin/env python

import sys
from monik.uwsgi import app

def parse_args():
    host = '127.0.0.1'
    port = 5000

    for arg in sys.argv[1:]:
        if arg.startswith('--host='):
            host = arg.split('=')[1]
        elif arg.startswith('--port='):
            port = int(arg.split('=')[1])
    return host, port

if __name__ == '__main__':
    host, port = parse_args()
    app.run(host=host, port=port)
