import json
import logging

from common.localthread_middleware import get_current_user_id
from common.localthread_middleware import get_txid

def log_event(event_name, log_data, logging_module="django_default", level="INFO"):
    """
    :param event_name: Event name which you are logging
    :param log_data: The data you want to log, this can be anything serializable
    :param logging_module: If you want to use any custom module for logging, define it in Django settings
    :param level: Level for which you are logging.
    """
    logger = logging.getLogger(logging_module)

    try:
        msg = {"ev": event_name, "data": log_data, "txid": get_txid()}
        user_id = get_current_user_id()
        if user_id:
            msg["uid"] = user_id
        logger.log(msg=json.dumps(msg), level=getattr(logging, level))
    except Exception as e:
        print('Error')  # user error monitoring tool
        return

