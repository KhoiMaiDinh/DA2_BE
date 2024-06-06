from flask_restx import fields
from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

from .extensions import api

image_model = api.model("Image", {
    "image": fields.Integer
})

image_parser = reqparse.RequestParser()
image_parser.add_argument('image', type=FileStorage, location='files', required=True)