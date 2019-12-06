from flask import Flask, jsonify, request, json
from flask_restful import Resource, reqparse
from .database_models import User, DataList, DataListItem
from datA import db, app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from validate_email import validate_email

parser = reqparse.RequestParser()
parser.add_argument('q',type=str, help="Search word")
parser.add_argument('limit',type=int, help="Limit can only be a number")
parser.add_argument('page',type=int, help="Page value can only be a number")


class RegisterUser(Resource): 
    """register a new user to the database"""

    def post(self):
        """post method for passing user credentials to the request"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', required=True, type=str,
                                help='please enter your first name.')
            parser.add_argument('second_name', required=True, type=str,
                                help='please enter your second name.')
            parser.add_argument('email', required=True, type=str,
                                help='please enter an email address.')
            parser.add_argument('password', required=True, type=str,
                                help='please enter a password.')
            args = parser.parse_args()
            if not args['first_name']:
                return {'message': 'First name should not be empty!'}, 400
            if not args['second_name']:
                return {'message': 'Second name should not be empty!'}, 400
            if not args['email']:
                return {'message': 'Email should not be empty!'}, 400
            if validate_email(args['email'], check_mx=True) == False:
                return {'message': 'Wrong email entered!'}, 400
            if not args['password']:
                return {'message': 'Password should not be empty!'}, 400
            if not len(args['password']) > 8:
                return {'message': "Password should be longer than 8 characters!"}, 400

            new_user = User(first_name=args['first_name'], second_name=args['second_name'],
                            email=args['email'], password=args['password'])
            if User.query.filter_by(email=args['email']).first():
                return {'message': 'User you are entering already exists!'}, 409
            else:
                if (re.match('[a-zA-Z]', args['first_name'])
                   and re.match('[a-zA-Z]', args['second_name'])):
                    new_user.save()
                    return {'message': 'Successfully registered new user!'}, 201
                else:
                    return {'message': 'first name or second name can not contain\
                                        special characters or numbers!'}, 400
        except Exception as e:
            return {'message': 'User not registered due to errors! '+str(e)}, 400

class LoginUser(Resource):
    """this logs in a user"""

    def post(self):
        """Method is responsible for logging in a user."""

        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, type=str, help='please enter an email address!')
        parser.add_argument('password', required=True, type=str, help='please enter a password!')
        args = parser.parse_args()
        email, password = args['email'], args['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.verify_password(password):
                token = {'access_token': create_access_token(identity=user.email)}
                return {'message': 'Successfully logged in', 'token': token }, 201
            else:
                return {'message': 'You entered a wrong password!'}, 400
        else:
            return {'message': 'User does not exist!'}, 404

class SingleDatalist(Resource):
    """Class responsible for fetching, editing and deleting a specific data
    list.
    """

    @jwt_required
    def get(self, ID):
        """method fetches a specific data list by its ID"""

        datalist = DataList.query.filter_by(id=ID).first()
        if datalist:
            items = DataListItem.query.filter_by(data_list_it_belongs_to=datalist.name).all()
            all_items = []
            for item in items:
                item_and_details = {
                    'id': item.id,
                    'name': item.name,
                    'date_created': item.date_created,
                    'date_modified': item.date_modified,
                    'done': False
                }
                all_items.append(item_and_details)

            data_and_details = {
                'id': datalist.id,
                'name': datalist.name,
                'items': all_items,
                'date_created': datalist.date_created,
                'date_modified': datalist.date_modified,
                'created_by': datalist.created_by
                }

            return jsonify({'data list': data_and_details}, 200)

        else:
            return {'message': 'No data list with that given ID.'}, 404

    @jwt_required
    def delete(self, ID):
        """Method deletes a specified data list"""

        datalist = DataList.query.filter_by(id=ID).first()
        if datalist:
            datalist.delete()
            return {'message': 'Datalist deleted successfully'}, 200
        else:
            return {'message': 'No data list found with that ID'}, 404

    @jwt_required
    def put(self, ID):
        """Method edits a specified bucke list"""

        datalist = DataList.query.filter_by(id=ID).first()
        if datalist:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True, type=str,
                                help='please enter a data list name.')
            args = parser.parse_args()
            if args['name']:
                datalist.name = args['name']
                datalist.save()
                return {'message': 'Data list edit successful'}, 201

            else:
                return {'message': 'Please enter a name to replace the current one stored!'}, 400
        else:
            return {'message': 'No data list found with that ID'}, 404


class Datalist(Resource):
    """Create a data list"""

    @jwt_required
    def post(self):
        """method responsible for creating a data list."""

        user = User.query.filter_by(email=get_jwt_identity()).first()
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str,
                            help='please enter a data list name.')
        args = parser.parse_args()
        if args['name']:
            if (re.match('[a-zA-Z]', args['name'])):
                try:
                    datalist = DataList(name=args['name'], user_email=user.email)
                    datalist.save()
                    return {'message': '{} has been added to your pool of data\
                                        lists.'.format(args['name'])}, 201
                except:
                    return {'message': 'Data list already exists!'}, 409
            else:
                    return {'message': 'Datalist name can not contain\
                                        special characters or numbers!'}, 400
        else:
            return {'message': 'Please provide a name for the data list.'}, 400

    @jwt_required
    def get(self):
        """method responsible for fetching all data lists."""

        args = parser.parse_args()
        limit = 20
        qword = None
        page = 1
        
        if args['limit']:
            limit = int(args['limit'])
            if limit < 1:
                limit = 20
            if limit > 100:
                limit = 100

        if args['q']:
            qword = args['q']
            if qword is None or qword =="":
                qword = None
        
        if args['page']:
            page = int(args['page'])
            if page < 1:
                page =1

        user = User.query.filter_by(email=get_jwt_identity()).first()
        page = (page - 1) * limit
        
        if qword:
            qword = "%{}%".format(qword)
            datalist = DataList.query.filter(DataList.name.ilike(qword)).filter(DataList.created_by==user.email).offset(page).limit(limit).all()
        else:
            datalist = DataList.query.filter_by(created_by=user.email).offset(page).limit(limit).all()
        output = {}
        if datalist:
            datas = []
            for data in datalist:
                items = DataListItem.query.filter_by(data_list_it_belongs_to=data.name).all()
                all_items = []
                for item in items:
                    item_and_details = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified,
                        'done': False
                    }
                    all_items.append(item_and_details)

                data_and_details = {
                    'id': data.id,
                    'name': data.name,
                    'items': all_items,
                    'date_created': data.date_created,
                    'date_modified': data.date_modified,
                    'created_by': data.created_by
                }

                datas.append(data_and_details)

            return jsonify({'datas': datas}, 200)

        else:
            return {'message': 'No data lists at the moment!'}, 404


class DatalistItem(Resource):
    """class responsible for creating data list items"""

    @jwt_required
    def post(self, ID):
        """Method/view creates an item and adds it to a data list"""

        datalist = DataList.query.filter_by(id=ID).first()
        if datalist:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True, type=str, help='please enter an item name!')
            args = parser.parse_args()
            item_name = args['name']
            if item_name:
                single_item = DataListItem.query.filter_by(data_list_it_belongs_to=datalist.name).all()
                if single_item:
                    for an_item in single_item:
                        if an_item.name != item_name:
                            new_item = DataListItem(name=item_name)
                            new_item.data_list_it_belongs_to = datalist.name
                            new_item.save()
                            return {'message': 'Item saved successfully.'}, 201
                        else:
                            return {'message': 'The item you are trying to add already exists!'}, 409
                else:
                    new_item = DataListItem(name=item_name)
                    new_item.data_list_it_belongs_to = datalist.name
                    new_item.save()
                    return {'message': 'Item saved successfully.'}, 201
            else:
                return {'message': 'Please provide an item name'}, 400
        else:
            return {'message': 'Data list you are trying to add to does not exist'}, 404

class SingleDatalistItem(Resource):
    """Class works on a single item"""

    @jwt_required
    def put(self, ID_data, ID_item):
        """This view edits a given data list item"""

        datalist = DataList.query.filter_by(id=ID_data).first()
        if datalist:
            items = DataListItem.query.filter_by(data_list_it_belongs_to=datalist.name).all()
            for item in items:
                if item.id == ID_item:
                    parser = reqparse.RequestParser()
                    parser.add_argument('name', required=True, type=str,
                                        help='please enter an item name!')
                    args = parser.parse_args()
                    item_name = args['name']
                    if item_name:
                        item.name = item_name
                        item.save()
                        return {'message': 'Item edited successfully.'}, 201
                    else:
                        return {'message': 'Please provide an item name.'}, 400
                else:
                    return {'message': 'No item with the given ID!'}, 404
        else:
            return {'message': 'Data list with that ID doesnt exist!'}, 404

    @jwt_required
    def delete(self, ID_data, ID_item):
        """This view deletes a gicen data list item."""

        datalist = DataList.query.filter_by(id=ID_data).first()
        items = DataListItem.query.filter_by(data_list_it_belongs_to=datalist.name).all()
        for item in items:
            if item.id == ID_item:
                item.delete()
                return {'message': 'Item has been deleted successfully!'}, 200
            else:
                return {'message': 'No item found with that ID!'}, 404

