import datetime

import flask
from flask import jsonify, request

from . import db_session
from . jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


# Получение всех работ
@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size',
                                    'collaborators', 'start_date', 'end_date',
                                    'is_finished', 'user.name'))
                 for item in jobs]
        }
    )


# Получение одной работы
@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs':
                jobs.to_dict(only=('team_leader', 'job', 'work_size',
                                    'collaborators', 'start_date', 'end_date',
                                    'is_finished', 'user.name'))
        }
    )


# Добавление работы
@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators']):
        return jsonify({'error': 'Bad request'})
    elif 'id' in request.json:
        if 'jobs' in get_one_jobs(request.json['id']).json:
            return jsonify({'error': 'Id already exists'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators']
    )
    # Если есть поля по умолчанию
    if 'is_finished' in request.json:
        jobs.is_finished = request.json['is_finished']
    if 'start_date' in request.json:
        jobs.start_date = request.json['start_date']
    else:
        jobs.start_date = datetime.datetime.now()
    if 'end_date' in request.json:
        jobs.end_date = request.json['end_date']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# Удаление работы
@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# Редактирование работы
@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators',
                  'is_finished', 'start_date', 'end_date']):
        return jsonify({'error': 'Bad request'})

    if 'team_leader' in request.json:
        jobs.team_leader = request.json['team_leader']
    if 'job' in request.json:
        jobs.job = request.json['job']
    if 'work_size' in request.json:
        jobs.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        jobs.collaborators = request.json['collaborators']

    # Если есть поля по умолчанию
    if 'is_finished' in request.json:
        jobs.is_finished = request.json['is_finished']
    if 'start_date' in request.json:
        jobs.start_date = request.json['start_date']
    else:
        jobs.start_date = datetime.datetime.now()
    if 'end_date' in request.json:
        jobs.end_date = request.json['end_date']

    db_sess.commit()
    return jsonify({'success': 'OK'})
