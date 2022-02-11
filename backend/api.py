from cmath import log
import re
import flask
import redis
import os

from CrosswordGenerator import getClueList, getCrossword, getGridList
from GridGenerator import printGrid

import logging

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    logging.info("Starting generation")
    grid, words = getCrossword()
    words = getClueList()
    logging.info("word list made")
    grid = getGridList()
    logging.info("Grid list made")
    logging.info("TESTING")

    #print('\n'.join([''.join(['{:4}'.format(str(item['acrossNumber'])+ '|' +str(item['downNumber'])) for item in row]) for row in grid]))

    response = flask.jsonify({'words':words, 'grid': grid})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.errorhandler(404)
def page_not_found(e):
    response = flask.jsonify("<h1>404</h1><p>The resource could not be found.</p>", 404)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 404

if __name__ == "__main__":
    # Connect to redis client
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = os.environ.get("REDIS_PORT", 6379)
    redis_password = os.environ.get("REDIS_PASSWORD", None)
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)

    app.run(port=8080, host='0.0.0.0')