from flask import Flask
from flask_cors import CORS, cross_origin

from .extensions import api
from .resources import ns


# def create_app():
app = Flask(__name__)
cors = CORS(app)

api.init_app(app)

api.add_namespace(ns)

    
if __name__ == '__main__':
    app.run()