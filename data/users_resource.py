from datetime import datetime

from flask import jsonify
from flask_restful import abort, Resource

from .users import User
from .users_parser import parser, put_parser
from . import db_session


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, error=f"User {users_id} not found")


def abort_if_users_exist(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if users:
        abort(404, error=f"User {users_id} already exists")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({'users': users.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality',
                  'address', 'modified_date'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, users_id):
        abort_if_users_not_found(users_id)
        args = put_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        if not args:
            abort(404, error=f"Bad request.")
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        if 'surname' in args:
            users.surname = args['surname']
        if 'name' in args:
            users.name = args['name']
        if 'age' in args:
            users.age = args['age']
        if 'position' in args:
            users.position = args['position']
        if 'speciality' in args:
            users.speciality = args['speciality']

        # Если есть поля по умолчанию
        if 'modified_date' in args:
            users.modified_date = args['modified_date']
        else:
            users.modified_date = datetime.now()
        if 'hashed_password' in args:
            users.set_password(args['hashed_password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality',
                  'address', 'modified_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if 'id' in args:
            abort_if_users_exist(args['id'])
        users = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address']
        )
        if 'modified_date' in args:
            users.modified_date = args['modified_date']
        else:
            users.modified_date = datetime.now()
        if 'hashed_password' in args:
            users.set_password(args['hashed_password'])
        else:
            users.set_password('123456')
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
