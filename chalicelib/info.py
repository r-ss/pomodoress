from datetime import datetime
import os
import platform

from chalicelib.misc import current_time
from chalicelib.ssm_parameter import SSMParameter

from chalicelib.config import Config

def readinfo():
    """ Return basic system information and variables, like is app runs
        in production mode or not. Might be useful on deployment.
        Can be used for fast status check in production

        access via /info url
    """

    load1, load5, load15 = os.getloadavg()

    return {
        'resource': 'pomodoress',
        'datetime_now': datetime.now().strftime('%d %B %Y %H:%M:%S'),
        'datetime_utcnow': datetime.utcnow().strftime('%d %B %Y %H:%M:%S'),
        'special_current_time': current_time(),
        'ssm_parameter': SSMParameter.get(),
        'env_teststring': os.environ.get('TESTSTRING'),
        'telegram_enabled': Config.TELEGRAM_ENABLED,
        'os': os.name,
        'platform': platform.system(),
        'platform_release': platform.release(),
        'python version': platform.python_version(),
        'testing': Config.TESTING_MODE,
        'production': Config.PRODUCTION,
        'load averages': f'{load1:.2f} {load5:.2f} {load15:.2f}'
    }
