from flask import request, send_from_directory
from flask_restx import marshal, Resource
from werkzeug.utils import secure_filename

from app import app, api
from ad_insertion_executor import ad_insertion_executor
from flask import request
from flask_restx import marshal, Resource

from app import app, api
from src import serializers
from ad_insertion_executor import ad_insertion_executor


@api.route('/conf')
class ConfigurationResource(Resource):
    @staticmethod
    def get() -> dict:
        """ Get current model configuration """

        return marshal(app.config['model_config'], serializers.conf_serializer)

    @api.expect(serializers.conf_serializer)
    def put(self) -> dict:
        """ Update model configuration """

        app.config['model_config'].update(request.get_json())
        app.save_conf()
        return marshal(app.config['model_config'], serializers.conf_serializer)


@api.route('/processing')
class ProcessingResource(Resource):

    @api.expect(serializers.processing_serializer)
    def post(self):
        """ Process new files, return processed video """

        payload = request.get_json()
        ad_insertion_executor(payload['video_path'], payload['logo_path'], app.conf_path)
        finish = 'Video file has been processed.'
        return finish
