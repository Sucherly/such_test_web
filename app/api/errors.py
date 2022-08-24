from flask import jsonify


def bad_request(message):
    response = jsonify({'error': 'bad request', 'msg': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'msg': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'msg': message})
    response.status_code = 403
    return response


def internal_server_error(message):
    response = jsonify({'error': 'Internal Server Error', 'msg': message})
    response.status_code = 500
    return response



