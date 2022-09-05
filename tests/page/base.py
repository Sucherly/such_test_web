from base64 import b64encode

from flask import jsonify


class Base:
    def __init__(self):
        pass

    def get_token(self, username, password):
        """获取token"""
        return 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')

    def get_api_headers(self, username, password):
        """获取账号认证信息"""
        return {
            'Authorization': self.get_token(username,password),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def option_ok(self,data, message=None, **kwargs):
        """ok"""
        message = message or '操作成功！'
        data_dic = {'code': 200, 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def field_superfluous(self,data, message=None, **kwargs):
        """存在多余的字段"""
        message = message or '请求成功，操作已处理，但存在多余的字段未处理。'
        data_dic = {'code': 20001, 'error': 'field superfluous', 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def option_null(self,data, message=None, **kwargs):
        """插入的数据未查询到"""
        message = message or '插入的数据未查询到！'
        data_dic = {'code': 20002, 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def duplicated(self,data, message=None,**kwargs):
        """重复"""
        message = message or '请求成功，但是在处理时数据重复，不进行操作。'
        data_dic = {'code': 50001, 'error': 'duplicated', 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def malformation(self,data, message=None,**kwargs):
        """格式错误"""
        message = message or '请求成功，但请求的数据存在格式错误，不进行操作。'
        data_dic = {'code': 50002, 'error': 'malformation', 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def content_wrong(self,data, message=None,**kwargs):
        """内容错误"""
        message = message or '请求成功，但请求的数据存在错误，例如内容为空、或缺少某个必要字段，不进行操作。'
        data_dic = {'code': 50004, 'error': 'Content Wrong', 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def not_fund(self,data, message=None,**kwargs):
        """数据未找到"""
        message = message or '数据未找到！'
        data_dic = {'code': 500404, 'error': 'data_not_fund', 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def api_response(self,data, message=None, code=200, **kwargs):
        message = message or '请求成功!'
        data_dic = {'code': code, 'msg': message, 'data': data}
        if kwargs:
            data_dic.update(kwargs)
        return data_dic

    def time_to_gmt(self,data):
        """转换成GMT格式"""
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        return data.strftime(GMT_FORMAT)