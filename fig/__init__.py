from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException
from logging.config import dictConfig
from grpc import FutureTimeoutError
from flask_limiter import Limiter
from flask import Flask, jsonify
from olive.exc import GRPCError
import traceback
import logging


app = Flask(import_name=__name__)
app.config.from_json('/etc/fig/fig.json')

# TODO change key_func to a custom function to limit based on user_id
# TODO then fallback on ip address
rate_config = app.config['RATE_LIMIT']
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=rate_config['default_rule'],
    storage_uri=rate_config['storage_uri']
)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': app.config['LOGGING']['formatter'],
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': app.config['LOGGING']['level'],
        'handlers': ['wsgi']
    }
})

app.logger.setLevel(logging.DEBUG)


@app.errorhandler(Exception)
def handle_error(e):
    app.logger.debug('Exception: {}'.format(type(e)))
    app.logger.error(traceback.format_exc())
    err = app.config['ERRORS']
    code = err['server_error']['code']
    reason = err['server_error']['reason']
    details = []
    status_code = 500
    if isinstance(e, HTTPException):
        status_code = e.code
        if str(status_code) in err:
            code = err[str(status_code)]['code']
            reason = err[str(status_code)]['reason']
        else:
            app.logger.error('@TODO status code {} needs to be added in error config'.format(status_code))
    elif isinstance(e, GRPCError):
        details = [] if not e.errors.details else list(e.errors.details)
        code = e.errors.code
        reason = err['service_error']['reason']
        if code in err:
            code = err[code]['code']
            reason = err[code]['reason']
            status_code = err[code]['status_code']
        else:
            app.logger.error('@TODO code {} needs to be added in error config'.format(code))
    elif isinstance(e, FutureTimeoutError):
        code = err['future_timeout']['code']
        reason = err['future_timeout']['reason']
        status_code = err['future_timeout']['status_code']
    else:
        pass

    return jsonify({'error': {
        'code': code,
        'reason': reason,
        'details': details
    }}), status_code
