import requests
from flask import request

from app import db
from app.api import api
from app.api.check_info import option_ok, api_response
from app.models import Production, ProInterface


@api.route('/productions', methods=['GET',"POST"])
def get_productions():
    """获取所有产品"""
    res = Production.query.all()
    data = [dt.to_json() for dt in res]
    return option_ok(data)


@api.route('/production/product=<int:product>', methods=['GET'])
def get_product_by_id(product):
    """根据id获取产品"""
    res = Production.query.filter_by(id=product).first_or_404()
    return option_ok(res.to_json())


@api.route('/interfaces/product=<int:product>', methods=['GET'])
def get_api_by_product(product):
    """根据产品id获取所有接口"""
    res = ProInterface.query.filter_by(product=product).all()
    data = [dt.to_json() for dt in res]
    return option_ok(data)


@api.route('/productAPI', methods=['POST'])
def save_product_api():
    """新增或更新api"""
    data = request.json
    if 'id' not in data:
        # 新增
        interface = ProInterface()
    else:
        # 更新
        interface = ProInterface.query.filter_by(id=data['id']).first_or_404()
    for k, v in data.items():
        if hasattr(ProInterface, k):
            setattr(interface, k, v)
    db.session.add(interface)
    db.session.commit()
    # 再次查询数据以返回
    if 'id' in data:
        res = ProInterface.query.filter_by(id=data['id']).first_or_404()
    else:
        res = ProInterface.query.filter_by(name=data['name']).first_or_404()
    return option_ok(res.to_json())


@api.route('/interface/id=<int:data_id>', methods=['GET'])
def get_api_by_id(data_id):
    """根据id获取接口"""
    res = ProInterface.query.filter_by(id=data_id).first_or_404()
    return option_ok(res.to_json())


@api.route('/interface/delete/id=<int:data_id>', methods=['GET'])
def delete_api_by_id(data_id):
    """根据id获取接口"""
    res = ProInterface.query.filter_by(id=data_id).first_or_404()
    # data=res.to_json()
    db.session.delete(res)
    db.session.commit()
    return option_ok(res.to_json(), message='删除成功！')


@api.route('/interface/run', methods=['POST'])
def run_api_by_id():
    """根据id运行接口"""
    data = request.json
    res = ProInterface.query.filter_by(id=data['id']).first_or_404()
    url_path = '/'.join(res.url.split('/')[0:-1])
    url_path += '/' + data['param']
    url = '{}{}'.format(data['url'], url_path)
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    payload = data['body'] or {}
    response = requests.request(res.request_type, url=url, headers=headers, params=payload)
    return api_response(response.text,code=response.status_code)
