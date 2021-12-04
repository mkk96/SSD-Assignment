from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/bill'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class menu(UserMixin, db.Model):
    '''Creating menu table'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    half_plate_price = db.Column(db.String(80), nullable=False)
    full_plate_price = db.Column(db.String(80), nullable=False)


class register(UserMixin, db.Model):
    '''creating Register table'''
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    chef = db.Column(db.Integer, nullable=False)


class transaction(UserMixin, db.Model):
    '''Creating transaction table'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    total_value = db.Column(db.Float, primary_key=True, autoincrement=False)
    tip_value = db.Column(db.Integer, primary_key=True, autoincrement=False)
    discount = db.Column(db.Float, primary_key=True, autoincrement=False)
    each_person_share = db.Column(
        db.Float,
        primary_key=True,
        autoincrement=False)
    final_value = db.Column(db.Float, primary_key=True, autoincrement=False)


class transaaction_detail(UserMixin, db.Model):
    '''Creating transaction detail table'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    plate_type = db.Column(
        db.String(80),
        primary_key=True,
        autoincrement=False)
    quantity = db.Column(db.Integer, primary_key=True, autoincrement=False)
    item_total_value = db.Column(
        db.Float,
        primary_key=True,
        autoincrement=False)

class add_user(Resource):
    def post(self):
        '''After geting username & password from client now it add user
            into register table'''
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        check = register.query.filter_by(username=username).first()
        if check is not None:

            return 0
        else:
            obj = register(username=username, password=password, chef=2)
            db.session.add(obj)
            db.session.commit()
            return 1


class login_user(Resource):
    def post(self):
        '''Authenticate participant it is valid user or not'''
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        user_detail = register.query.filter_by(username=username).first()
        if user_detail is None:
            return 0
        elif user_detail.password != password:
            return 0
        else:
            return user_detail.chef


class menu_display(Resource):
    '''After geting requst from client it connect to menu table and connect 
        menu table to get menu'''
    def get(self):
        menu_item = menu.query.all()
        menu_item_json = {}
        if len(menu_item) == 0:
            return "No Menu to Display yet"
        for item in menu_item:
            menu_item_json[str(item.id)] = {
                "id": item.id,
                "half": item.half_plate_price,
                "full": item.full_plate_price}
        return jsonify(menu_item_json)


class add_new_menu_item(Resource):
    def post(self):
        '''Adding new menu item after getting request from chef'''
        posted_data = request.get_json()
        new_menu_item = posted_data['data']
        for item in new_menu_item:
            obj = menu(
                id=item[0],
                half_plate_price=item[1],
                full_plate_price=item[2])
            db.session.add(obj)
        db.session.commit()


class trans_detail(Resource):
    def post(self):
        '''Adding each transaction detail of a user in a detail'''
        posted_data = request.get_json()
        item_list = posted_data['data']
        number = transaction.query.filter_by(username=item_list[0][0])
        trans_id = 0
        if number is None:
            trans_id = 1
        else:
            trans_id = number.count() + 1
        for item in item_list:
            obj = transaaction_detail(
                id=trans_id,
                username=item[0],
                item_id=item[1],
                plate_type=item[2],
                quantity=item[3],
                item_total_value=item[4])
            db.session.add(obj)
        db.session.commit()


class trans(Resource):
    def post(self):
        '''Adding user detail of a user'''
        posted_data = request.get_json()
        item_list = posted_data['data']
        number = transaction.query.filter_by(username=item_list[0])
        trans_id = 0
        if number is None:
            trans_id = 1
        else:
            trans_id = number.count() + 1
        obj = transaction(
            id=trans_id,
            username=item_list[0],
            total_value=item_list[1],
            tip_value=item_list[2],
            discount=item_list[3],
            each_person_share=item_list[4],
            final_value=item_list[5])
        db.session.add(obj)
        db.session.commit()


class get_trans(Resource):
    def post(self):
        '''Getting each transaction detail of a user in a detail'''
        posted_data = request.get_json()
        user = posted_data['username']
        trans_item = transaction.query.filter_by(username=str(user)).all()
        if trans_item is None:
            return jsonify("{}")
        else:
            trans_item_json = {}
            for item in trans_item:
                trans_item_json[str(item.id)] = {"total": item.total_value,
                                                 "tip": item.tip_value,
                                                 "discount": item.discount,
                                                 "each": item.each_person_share,
                                                 "final_total": item.final_value}
            return jsonify(trans_item_json)


class get_trans_detail(Resource):
    def post(self):
        '''getting user detail of a user'''
        posted_data = request.get_json()
        username = posted_data['username']
        trans_id = posted_data['trans_id']
        trans_detail_list = transaaction_detail.query.filter_by(
            username=username, id=trans_id).all()
        trans_detail_list_json = {}
        count = 0
        for item in trans_detail_list:
            trans_detail_list_json[str(count)] = {"id": item.item_id,
                                                  "plate": item.plate_type,
                                                  "quantity": item.quantity,
                                                  "item_value": item.item_total_value}
            count = count + 1
        return jsonify(trans_detail_list_json)


api.add_resource(add_user, '/add_user')
api.add_resource(login_user, '/login_user')
api.add_resource(menu_display, '/menu_display')
api.add_resource(add_new_menu_item, '/add_new_menu_item')
api.add_resource(trans_detail, '/trans_detail')
api.add_resource(trans, '/trans')
api.add_resource(get_trans, '/get_trans')
api.add_resource(get_trans_detail, '/get_trans_detail')
if __name__ == '__main__':
    db.create_all()
    app.run(port=8000, debug=True)
