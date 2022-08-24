from flask import jsonify


def option_ok(data, message=None, **kwargs):
    """ok"""
    message = message or '操作成功！'
    data_dic = {'msg': message, 'data': data}
    if kwargs:
        data_dic.update(kwargs)
    response = jsonify(data_dic)
    response.status_code = 200
    response.message = 'OK'
    return response


def field_superfluous(data, message=None, **kwargs):
    """存在多余的字段"""
    message = message or '请求成功，操作已处理，但存在多余的字段未处理。'
    data_dic = {'error': 'field superfluous', 'msg': message, 'data': data}
    if kwargs:
        data_dic.update(kwargs)
    response = jsonify(data_dic)
    response.status_code = 20001
    response.message = '存在多余的字段'
    return response


def option_null(data, message=None, **kwargs):
    """插入的数据未查询到"""
    message = message or '插入的数据未查询到！'
    data_dic = {'msg': message, 'data': data}
    if kwargs:
        data_dic.update(kwargs)
    response = jsonify(data_dic)
    response.status_code = 20002
    return response


def duplicated(data, message=None):
    """重复"""
    message = message or '请求成功，但是在处理时数据重复，不进行操作。'
    response = jsonify({'code': 50001, 'error': 'duplicated', 'msg': message, 'data': data})
    response.status_code = 50001
    response.message = 'duplicated'
    return response


def malformation(data, message=None):
    """格式错误"""
    message = message or '请求成功，但请求的数据存在格式错误，不进行操作。'
    response = jsonify({'code': 50002, 'error': 'malformation', 'msg': message, 'data': data})
    response.status_code = 50001
    return response


def content_wrong(data, message=None):
    """内容错误"""
    message = message or '请求成功，但请求的数据存在错误，例如内容为空、或缺少某个必要字段，不进行操作。'
    response = jsonify({'error': 'Content Wrong', 'msg': message, 'data': data})
    response.status_code = 50004
    return response


def not_fund(data, message=None):
    """数据未找到"""
    message = message or '数据未找到！'
    response = jsonify({'error': 'data_not_fund', 'msg': message, 'data': data})
    response.status_code = 500404
    return response


def api_response(data, message=None, code=200, **kwargs):
    message = message or '请求成功!'
    data_dic = {'code':code,'msg': message, 'data': data}
    response = jsonify(data_dic)
    response.status_code = 200
    if kwargs:
        for k, v in kwargs.items():
            setattr(response, k, v)
    return response
