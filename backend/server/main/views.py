from server.main.rq_helpers import queue
from flask import Blueprint, jsonify, request
from server.main import jobs
import logging

main_blueprint = Blueprint("main", __name__, template_folder='templates')


@main_blueprint.route("/crossword/", methods=['GET', 'POST'])
def home():
    width = request.args.get('width', default=10, type = int)
    length = request.args.get('length', default=10, type = int)
    job = jobs.crossword.delay(width, length)
    response_object = jsonify({
        "status": "success",
        "data": {
            "job_id": job.get_id()
        }
    })
    response_object.headers.add('Access-Control-Allow-Origin', '*')
    return response_object, 202



@main_blueprint.route("/jobs/<job_id>", methods=["GET"])
def get_status(job_id):
    job = queue.fetch_job(job_id)
    if job:
        response_object = {
            "status": "success",
            "data": {
                "job_id": job.get_id(),
                "job_status": job.get_status(),
                "job_result": job.result,
            },
        }
        status_code = 200
    else:
        response_object = {"status": "error"}
        status_code = 500

    response_object = jsonify(response_object)
    response_object.headers.add('Access-Control-Allow-Origin', '*')
    return response_object, status_code
