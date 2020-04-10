
import logging
import ldap
import json
from flask.views import MethodView
from apps.api.util import authenticate, filter_group

from . import bp


class ActiveDirectoryGroup(MethodView):
    SCHEMA_UPLOAD = {
        'file': {
            'type': 'filestorage',
            'required': True
        }
    }

    def __init__(self):
        super().__init__()

    def post(self):
        return "POST"

    def get(self):
        ad_conn = authenticate(
            "192.168.122.134",
            "esadmin@esdemo.editshare.com",
            "Changeme0479"
        )
        result = filter_group(
            group_name="esusers",
            ad_conn=ad_conn,
            basedn="OU=editshare, DC=esdemo, DC=editshare, DC=com"
        )
        return json.dumps(result)


bp.add_url_rule(
    '/group',
    view_func=ActiveDirectoryGroup.as_view('active_directory_group')
)
