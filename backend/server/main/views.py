
from server.main.rq_helpers import queue
from flask import render_template, Blueprint, jsonify, request, current_app, redirect
from server.main.CrosswordGenerator import getCrossword, getClueList, getGridList
from server.main import jobs
import logging

main_blueprint = Blueprint("main", __name__, template_folder='templates')


@main_blueprint.route("/", methods=["GET"])
def home():
    width = request.args.get('width', default=10, type = int)
    length = request.args.get('length', default=10, type = int)
    queue.enqueue(jobs.crossword, width, length, on_success=report_success, on_failure=report_failure)

    #print('\n'.join([''.join(['{:4}'.format(str(item['acrossNumber'])+ '|' +str(item['downNumber'])) for item in row]) for row in grid]))


def report_success(job, connection, result, *args, **kwargs):
    response = jsonify({'words':result[0], 'grid': result[1]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    logging.info("SUCCESS")
    return response, 200


def report_failure(job, connection, type, value, traceback):
    logging.info("FAILURE")
    return {'words': {}, 'grid': []}, 400
