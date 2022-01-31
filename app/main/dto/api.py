from flask_restx import fields


def produce_api_response_structure(payload_structure, is_list=False):
    return {
        'is_success': fields.Boolean(required=True),
        'message': fields.String(),
        'payload': fields.List(fields.Nested(payload_structure)) if is_list else fields.Nested(payload_structure),
    }
