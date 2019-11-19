# -*- coding: utf-8 -*-
# pylint: disable=broad-except, bare-except

import base64
import traceback
import json
from .compat import s

try:
    import http.client as httplib
except:
    import httplib

from .const import (
    LOGGER
)

def exception_log(ex, _msg, *args):
    """Log exception"""
    msg = _msg.format(*args)
    try:
        msg += ", " + str(ex) + ", " + traceback.format_exc()
        LOGGER.exception(msg)
    except Exception as ex:
        LOGGER.error("**************************************** ERROR")

def shelly_http_get(host, url, username, password, log_error=True):
    """Send HTTP GET request"""
    res = ""
    success = False
    try:
        LOGGER.debug("http://%s%s", host, url)
        conn = httplib.HTTPConnection(host, timeout=2)
        headers = {}
        if username is not None \
            and password is not None:
            combo = '%s:%s' % (username, password)
            auth = s(
                base64.b64encode(combo.encode()))  # .replace('\n', '')
            headers["Authorization"] = "Basic %s" % auth
        conn.request("GET", url, None, headers)
        resp = conn.getresponse()

        if resp.status == 200:
            body = resp.read()
            LOGGER.debug("Body: %s", body)
            res = json.loads(s(body))
            success = True
        else:
            res = "Error, " + str(resp.status) \
                            + ' ' + str(resp.reason)
            LOGGER.debug(res)
        conn.close()
    except Exception as ex:
        success = False
        res = str(ex)
        if log_error:
            exception_log(ex, "Error http GET: http://{}{}", host, url)
        else:
            LOGGER.debug(
                "Fail http GET: %s %s %s", host, url, ex)

    return success, res