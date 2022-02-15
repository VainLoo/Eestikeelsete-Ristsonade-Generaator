
import logging
from flask import jsonify
from rq.decorators import job
from rq import get_current_job
from server.main.CrosswordGenerator import getClueList, getCrossword, getGridList
from server.main.rq_helpers import redis_connection
import time


# the timeout parameter specifies how long a job may take
# to execute before it is aborted and regardes as failed
# the result_ttl parameter specifies how long (in seconds)
# successful jobs and their results are kept.
# for more detail: https://python-rq.org/docs/jobs/
@job('default', connection=redis_connection, timeout=90, result_ttl=7*24*60*60)
def crossword(width, length):
    self_job = get_current_job()
    #grid, words = q.enqueue(getCrossword, length, width)
    grid, words = getCrossword(length, width)
    words = getClueList()
    logging.info("word list made")
    grid = getGridList()
    logging.info("Grid list made")
    logging.info("TESTING")

    #print('\n'.join([''.join(['{:4}'.format(str(item['acrossNumber'])+ '|' +str(item['downNumber'])) for item in row]) for row in grid]))

    #response = jsonify({'words':words, 'grid': grid})
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #self_job.save_meta()
    return (words, grid)
