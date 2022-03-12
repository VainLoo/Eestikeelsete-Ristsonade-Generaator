from server.main.rq_helpers import queue
from flask import Blueprint, jsonify
from server.main import jobs
import random
import logging


main_blueprint = Blueprint("main", __name__, template_folder='templates')
max_stored_results = 2400


@main_blueprint.route("/crossword/", methods=['GET'])
def home():
    #width = request.args.get('width', default=10, type = int)
    #length = request.args.get('length', default=10, type = int)
    print("finished count %s:" % queue.finished_job_registry.count)
    if queue.finished_job_registry.count > 0:
        doneJob = queue.fetch_job(random.choice(queue.finished_job_registry.get_job_ids()))
        #logging.info("LEITUD TULEMUS:",doneJob)
        response_object = {
            "status": "success",
            "data": {
                "job_id": doneJob.get_id(),
                "job_status": doneJob.get_status(),
                "job_result": doneJob.result,
            },
        }
        response_object = jsonify(response_object)
        response_object.headers.add('Access-Control-Allow-Origin', '*')
        queue.finished_job_registry.remove(doneJob, delete_job=True)
        CheckPremade()
        return response_object, 200
    else:
        CheckPremade()
        response_object = jsonify({
            "status": "success",
            "data": {   
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


def CheckPremade():
    effectiveJobsCount = queue.finished_job_registry.count + queue.started_job_registry.count + len(queue.get_job_ids())

    if effectiveJobsCount < max_stored_results:
        for i in range(max_stored_results-effectiveJobsCount):
            jobs.crossword.delay(random.randint(6, 12), random.randint(6, 12))


    logging.info('finished_job_registry %s' % queue.finished_job_registry.count)
    logging.info('started_job_registry %s' % queue.started_job_registry.count)
    logging.info('In queue: {}'.format(len(queue.get_job_ids())))
    logging.info("TOTAL: {}".format(effectiveJobsCount)) 

CheckPremade()