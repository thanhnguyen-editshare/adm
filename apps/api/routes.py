
import logging
from flask.views import MethodView

from . import bp
logger = logging.getLogger(__name__)


class ActiveDirectoryGroup(MethodView):
    SCHEMA_UPLOAD = {
        'file': {
            'type': 'filestorage',
            'required': True
        }
    }

    def post(self):
        return "POST"

    def get(self):
        return "GET"


bp.add_url_rule(
    '/group',
    view_func=ActiveDirectoryGroup.as_view('active_directory_group')
)
