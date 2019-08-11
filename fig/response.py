from flask import jsonify


class Response(object):
    def __init__(self):
        pass

    @staticmethod
    def success(result, pagination=None, status_code=200):
        # on success dictionary is returned,
        # flask-restful make a JSON response with the given status
        return {
            'result': result,
            'pagination': pagination or {},
            'error': {}
        }, int(status_code)

    @staticmethod
    def error(error, status_code=500):
        # on error flask-restful will be absent,
        # so we need to make a json response ourselves
        return jsonify({
            'result': {},
            'pagination': {},
            'error': error
        }), int(status_code)
