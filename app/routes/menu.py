from app import app,db
from flask import jsonify, request
from ..model.menu import Menu

@app.route('/api/menu/display/',methods=['GET'])
def display_menu():
    id = request.args['rest']
    menu = Menu.query.filter_by(restid=id)
    return jsonify(dishes=[i.serialize for i in menu])


@app.route('/api/menu/add/',methods=['POST'])
def add_dish():
    dish = request.args['name']
    desc = request.args['desc']
    price = request.args['price']
    restid= request.args['restid']
    add=Menu(dish=dish,description=desc,price=price,restid=restid)
    db.session.add(add)
    db.session.commit()
    return jsonify({"Done":"all set"})

