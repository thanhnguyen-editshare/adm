from werkzeug.exceptions import BadRequest

from cerberus import Validator
from flask import Response
import json

def validate_document(document, schema, **kwargs):
    """
    Validate `document` against provided `schema`
    :param document: document for validation
    :type document: dict
    :param schema: validation schema
    :type schema: dict
    :param kwargs: additional arguments for `Validator`
    :return: normalized and validated document
    :rtype: dict
    :raise: `BadRequest` if `document` is not valid
    """

    validator = Validator(schema, **kwargs)
    if not validator.validate(document):
        raise BadRequest(validator.errors)
    return validator.document


def json_response(doc=None, status=200):
    """
    Serialize document fetched from mongo and return flask response with applicaton/json mimetype.
    :param doc: document fetched from mongo
    :type doc: dict
    :param status: http respponse status
    :type status: int
    :return: flask http response
    :rtype: flask.wrappers.Response
    """

    return Response(json.JSONEncoder().encode(doc), status=status, mimetype='application/json')
