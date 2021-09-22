__version__ = '0.1.0'

#from flask import Flask
import flask
from flask import Flask
from waitress import serve
app = Flask(__name__)
@app.route('/api/v1/hello-world-15')
def myendpoint():
    status_code = flask.Response(status=200, response="Hello World 15")
    return status_code
serve(app, host='0.0.0.0', port=8080, threads=1) #WAITRESS!