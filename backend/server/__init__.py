import traceback
import flask
from flask import Flask
from server.main.views import main_blueprint
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions # exception handling


def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("server.config.ProductionConfig")
    app.register_blueprint(main_blueprint)


    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            status_code = 400
        else:
            status_code = 500

        message = str(e)
        print(traceback.format_exc())
        return flask.jsonify(message=message, error_traceback=traceback.format_exc()), status_code

    for ex in default_exceptions:
            app.register_error_handler(ex, handle_error)


    return app

app = create_app()
app.app_context().push()