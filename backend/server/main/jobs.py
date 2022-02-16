
import logging
from rq.decorators import job
from server.main.CrosswordGenerator import getClueList, getCrossword, getGridList
from server.main.rq_helpers import redis_connection



# the timeout parameter specifies how long a job may take
# to execute before it is aborted and regardes as failed
# the result_ttl parameter specifies how long (in seconds)
# successful jobs and their results are kept.
# for more detail: https://python-rq.org/docs/jobs/
@job('default', connection=redis_connection, timeout=9000, result_ttl=7*24*60*60)
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
