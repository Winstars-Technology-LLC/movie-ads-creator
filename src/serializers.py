from flask_restx import fields
from app import api

conf_serializer = api.model(
    'Configuration',
    {
        'min_area_threshold': fields.Integer,
        'contour_threshold': fields.Float,
    }
)
