"""
Знакомство с flask-sqlalchemy
Модель Марсиане
"""
import datetime

from flask import Flask

from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_user(surname, name, age, position, speciality, address, email):
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def add_job(team_leader, job_, work_size, collaborators, start_date, is_finished):
    job = Jobs()
    job.team_leader = team_leader
    job.job = job_
    job.work_size = work_size
    job.collaborators = collaborators
    job.start_date = start_date
    job.is_finished = is_finished

    db_sess = db_session.create_session()
    db_sess.add(job)
    db_sess.commit()

def main():
    db_session.global_init("db/mars_explorer.sqlite")

    # Добавляем капитана
    add_user("Scott", "Ridley", 21, "captain", "research engineer",
             "module_1", "scott_chief@mars.org")
    add_user("Solo", "Han", 28, "pilot", "repair engineer",
             "module_2", "solo_han@mars.org")
    add_user("Dameron", "Poe", 34, "pilot", "navigator",
             "module_2", "dameron_poe@mars.org")
    add_user("Windu", "Mace", 43, "Jedi Masters", "teacher",
             "module_3", "windu_mace@mars.org")

    # Первая работа
    add_job(1, "deployment of residential modules 1 and 2", 15, "2, 3", datetime.datetime.now(), False)

    app.run(port=8080, host='127.0.0.1')  # , debug=True)


if __name__ == '__main__':
    main()
