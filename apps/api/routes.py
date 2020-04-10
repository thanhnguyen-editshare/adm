
import logging
from flask.views import MethodView
from flask import current_app as app
from flask import request
import ast

from lib.utils import validate_document, json_response
from . import bp
logger = logging.getLogger(__name__)


class ActiveDirectoryGroup(MethodView):
    SCHEMA_GET = {
        'is_nested': {
            'type': 'boolean',
            'required': False,
            'allowed': [True, False],
            'default': False,
            'coerce': bool
        },
        'type': {
            'type': 'string',
            'required': False,
            'allowed': ["all", "user", "group"],
            'default': "all"
        }
    }

    def post(self):
        return "POST"

    def get(self, group_name):
        document = validate_document(
            request.args.to_dict(), self.SCHEMA_GET)
        rs = app.adm.group_search(
            group_name,
            is_nested=document['is_nested'],
            o_type=document['type']
        )
        return {"test":rs}


bp.add_url_rule(
    '/group/<group_name>',
    view_func=ActiveDirectoryGroup.as_view('active_directory_group')
)
