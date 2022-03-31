from datetime import datetime

from flask import jsonify
from flask_restful import abort, Resource

from .jobs import Jobs
from .jobs_parser import parser, put_parser
from . import db_session


def abort_if_jobs_not_found(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        abort(404, error=f"Jobs {job_id} not found")


def abort_if_jobs_exist(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if jobs:
        abort(404, error=f"Jobs {job_id} already exists")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_jobs_not_found(job_id)
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).get(job_id)
        return jsonify(
            {'jobs': jobs.to_dict(only=('team_leader', 'job', 'work_size',
                                        'collaborators', 'start_date',
                                        'end_date', 'is_finished',
                                        'user.name'))})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).get(job_id)
        db_sess.delete(jobs)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        abort_if_jobs_not_found(job_id)
        args = put_parser.parse_args()
        print(args)
        args = {k: v for k, v in args.items() if v is not None}
        print(args)
        if not args:
            abort(404, error=f"Bad request.")
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).get(job_id)
        if 'team_leader' in args:
            jobs.team_leader = args['team_leader']
        if 'job' in args:
            jobs.job = args['job']
        if 'work_size' in args:
            jobs.work_size = args['work_size']
        if 'collaborators' in args:
            jobs.collaborators = args['collaborators']

        # Если есть поля по умолчанию
        if 'is_finished' in args:
            jobs.is_finished = args['is_finished']
        if 'start_date' in args:
            jobs.start_date = args['start_date']
        else:
            jobs.start_date = datetime.now()
        if 'end_date' in args:
            jobs.end_date = args['end_date']

        db_sess.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {
                'jobs': [item.to_dict(only=('team_leader', 'job', 'work_size',
                                            'collaborators', 'start_date',
                                            'end_date', 'is_finished',
                                            'user.name')) for item in jobs]
            }
        )

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        if 'id' in args:
            abort_if_jobs_exist(args['id'])
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators']
        )
        # Если есть поля по умолчанию
        if 'is_finished' in args:
            jobs.is_finished = args['is_finished']
        if 'start_date' in args:
            jobs.start_date = args['start_date']
        else:
            jobs.start_date = datetime.now()
        if 'end_date' in args:
            jobs.end_date = args['end_date']
        db_sess.add(jobs)
        db_sess.commit()
        return jsonify({'success': 'OK'})
