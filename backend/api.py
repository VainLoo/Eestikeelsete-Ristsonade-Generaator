import re
import flask

from CrosswordGenerator import getClueDict, getCrossword, getGridList
from GridGenerator import printGrid

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    grid, words = getCrossword()
    dict = getClueDict()
    grid = getGridList()
    print("grid:", grid)
    #printGrid(grid)
    return grid#"<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()