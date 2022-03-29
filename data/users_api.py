import datetime

import flask
from flask import jsonify, request

from . import db_session
from . users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


# Получение всех пользователей
@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age',
                                    'position', 'speciality', 'address',
                                    'modified_date'))
                 for item in users]
        }
    )


# Получение одного пользователя
@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_users(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users':
                users.to_dict(only=('surname', 'name', 'age',
                                    'position', 'speciality', 'address',
                                    'modified_date'))
        }
    )


# Добавление пользователя
@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality',
                  'address']):
        return jsonify({'error': 'Bad request'})
    elif 'id' in request.json:
        if 'users' in get_one_users(request.json['id']).json:
            return jsonify({'error': 'Id already exists'})
    db_sess = db_session.create_session()
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address']
    )
    if 'modified_date' in request.json:
        users.modified_date = request.json['modified_date']
    else:
        users.modified_date = datetime.datetime.now()
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# Удаление пользователя
@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# Редактирование пользователя
@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def edit_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality',
                  'address', 'modified_date']):
        return jsonify({'error': 'Bad request'})

    if 'surname' in request.json:
        users.surname = request.json['surname']
    if 'name' in request.json:
        users.name = request.json['name']
    if 'age' in request.json:
        users.age = request.json['age']
    if 'position' in request.json:
        users.position = request.json['position']
    if 'speciality' in request.json:
        users.speciality = request.json['speciality']

    # Если есть поля по умолчанию
    if 'modified_date' in request.json:
        users.modified_date = request.json['modified_date']
    else:
        users.modified_date = datetime.datetime.now()

    db_sess.commit()
    return jsonify({'success': 'OK'})
