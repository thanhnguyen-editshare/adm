import os
from distutils.util import strtobool as _strtobool


def strtobool(value):
    try:
        return bool(_strtobool(value))
    except ValueError:
        return False


def env(variable, fallback_value=None):
    if os.environ.get('VIDEO_SERVER_USE_DEFAULTS'):
        return fallback_value

    env_value = os.environ.get(variable)
    if env_value is None:
        return fallback_value
    # Next isn't needed anymore
    elif env_value == "__EMPTY__":
        return ''
    else:
        return env_value


# base path
BASE_PATH = os.path.dirname(__file__)

#: logging
LOG_CONFIG_FILE = env('LOG_CONFIG_FILE', os.path.join(
    BASE_PATH, 'logging_config.yml'))

CORE_APPS = [
    'apps.swagger',
    'apps.api',
]

LDAP_URL = "ldap://esdemo.editshare.com"