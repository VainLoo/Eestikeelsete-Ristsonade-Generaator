
from server.main.CrosswordGenerator import getClueList, getCrossword, getGridList
from server.main.rq_helpers import redis_connection
from server.main.rq_helpers import queue
from rq.decorators import job
from rq import Retry
import logging

@job('default', connection=redis_connection, timeout=120, result_ttl=-1, retry=Retry(max=3))
def crossword(width, length):
    grid, words = getCrossword(length, width)
    logging.info("Crossword generated")
    words = getClueList()
    logging.info("word list made")
    grid = getGridList()
    logging.info("Grid list made")

    #print('\n'.join([''.join(['{:4}'.format(str(item['acrossNumber'])+ '|' +str(item['downNumber'])) for item in row]) for row in grid]))

    response = {'words':words, 'grid': grid}
    return response
