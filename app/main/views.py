from flask import render_template

from app.main import main
from app.models import ProInterface, Production


@main.route('/')
def index():
    return render_template('base_index.html')


@main.route('/production')
def production():
    return render_template('production/productions.html')


@main.route('/product_api/product=<int:product>', methods=["GET"])
def apis(product):
    res = Production.query.filter_by(id=product).first_or_404()
    return render_template('production/apis.html',data=res)


@main.route('/product_api/id=<int:data_id>', methods=["GET"])
def get_api_by_id(data_id):
    res = ProInterface.query.filter_by(id=data_id).first_or_404()
    # data = {k: getattr(res, k) for k in res.__dict__ if not k.startswith('_')}
    return render_template('production/api.html', data=res)
