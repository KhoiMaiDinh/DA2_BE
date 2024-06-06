from flask_restx import Resource, Namespace
import numpy as np
import cv2
from io import BytesIO

from .api_models import image_model, image_parser
from .detecting_method.selfblended.image_predict import main
from .detecting_method.cnnDetection.validate import main_cnn
from .detecting_method.universalFake.image_predict import validate

ns = Namespace("api/method")

@ns.route("/self_blended")
class SelfBlended(Resource):
    @ns.expect(image_parser)
    def post(self):
        args = image_parser.parse_args()
        uploaded_file = args['image']  # This is FileStorage instance
        img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        res = main(img)
        return {'fakeness': res}, 200
    
@ns.route("/cnn")
class CNN(Resource):
    @ns.expect(image_parser)
    def post(self):
        args = image_parser.parse_args()
        uploaded_file = args['image']  # This is FileStorage instance
        # img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        res = main_cnn(uploaded_file)
        return {'fakeness': res}, 200
    
@ns.route("/universal_fake")
class UniversalFake(Resource):
    @ns.expect(image_parser)
    def post(self):
        args = image_parser.parse_args()
        uploaded_file = args['image']  # This is FileStorage instance
        res = validate(uploaded_file)
        return {'fakeness': res}, 200
    
@ns.route("/average")
class Average(Resource):
    @ns.expect(image_parser)
    def post(self):
        args = image_parser.parse_args()
        uploaded_file = args['image']  # This is FileStorage instance
        copied_file_1 = BytesIO(uploaded_file.getvalue())
        copied_file_2 = BytesIO(uploaded_file.getvalue())
        copied_file_3 = BytesIO(uploaded_file.getvalue())
        uni = validate(copied_file_1)
        cnn = main_cnn(copied_file_2)
        img = cv2.imdecode(np.fromstring(copied_file_3.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        self_bld = main(img)
        res = (uni + cnn +  2 * self_bld) / 4
        return {'fakeness': res}, 200