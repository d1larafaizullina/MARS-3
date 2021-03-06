import datetime
import os

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from flask_restful import Api
from werkzeug.exceptions import abort

from forms.loginform import LoginForm
from forms.user import RegisterForm
from forms.job import JobsForm
from forms.department import DepartmentForm
from data import db_session, jobs_api, users_api
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.my_json_encoder import MyJSONEncoder
# api v2 (flask_restful)
from data import users_resource
from data import jobs_resource


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.json_encoder = MyJSONEncoder
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
api = Api(app)  # api v2 (flask_restful)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()  # filter(News.is_private != True)
    return render_template("index.html", jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email ==
                                          form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        add_user(form.surname.data, form.name.data, form.age.data,
                 form.position.data, form.speciality.data, form.address.data,
                 form.email.data, form.password.data)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def add_user(surname, name, age, position, speciality,
             address, email, password="123456"):
    user = User(
        surname=surname,
        name=name,
        age=age,
        position=position,
        speciality=speciality,
        address=address,
        email=email
    )
    user.set_password(password)

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobsForm()
    if form.validate_on_submit():
        add_job(form.team_leader.data, form.job.data, form.work_size.data,
                form.collaborators.data, datetime.datetime.now(),
                form.is_finished.data)
        return redirect('/')
    return render_template('addjob.html', title='Adding a Job', form=form)


def add_job(team_leader, job_, work_size,
            collaborators, start_date, is_finished):
    db_sess = db_session.create_session()
    job = Jobs(
        team_leader=team_leader,
        job=job_,
        work_size=work_size,
        collaborators=collaborators,
        start_date=start_date,
        is_finished=is_finished
    )
    db_sess.add(job)
    db_sess.commit()


@app.route('/jobs/<int:_id>', methods=['GET', 'POST'])
@login_required
def edit_job(_id):
    form = JobsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs). \
            filter(Jobs.id == _id,
                   (Jobs.user == current_user) |
                   (current_user.id == Jobs.team_leader) |
                   (current_user.id == 1)).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs). \
            filter(Jobs.id == _id,
                   (Jobs.user == current_user) |
                   (current_user.id == Jobs.team_leader) |
                   (current_user.id == 1)).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.is_finished = form.is_finished.data
            # db_sess.update(job)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/job_delete/<int:_id>', methods=['GET', 'POST'])
@login_required
def job_delete(_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == _id,
                                     (Jobs.user == current_user) |
                                     (current_user.id == Jobs.team_leader) |
                                     (current_user.id == 1)).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments")
def all_departments():
    db_sess = db_session.create_session()
    # departments = db_sess.query(Department).all()
    data = db_sess.query(Department, User).join(User).all()
    return render_template("departments.html", data=data)


@app.route('/adddepartment', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('adddepartment.html', title='Adding a Department', form=form)


@app.route('/departments/<int:dep_id>', methods=['GET', 'POST'])
@login_required
def edit_departments(dep_id):
    form = DepartmentForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        dep = db_sess.query(Department). \
            filter(Department.id == dep_id,
                   (current_user.id == Department.chief) |
                   (current_user.id == 1)).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department). \
            filter(Department.id == dep_id,
                   (current_user.id == Department.chief) |
                   (current_user.id == 1)).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('adddepartment.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/dep_delete/<int:dep_id>', methods=['GET', 'POST'])
@login_required
def department_delete(dep_id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == dep_id,
                                     (current_user.id == Department.chief) |
                                     (current_user.id == 1)).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': '404 - Not found'}), 404)


def main():
    db_exist = os.path.exists("db/mars_explorer.sqlite")
    db_session.global_init("db/mars_explorer.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)

    # Добавляем капитана, по умолчанию password="123456"
    if not db_exist:
        add_user("Scott", "Ridley", 21, "captain", "research engineer",
                 "module_1", "scott_chief@mars.org")
        add_user("Solo", "Han", 28, "pilot", "repair engineer",
                 "module_2", "solo_han@mars.org")
        add_user("Dameron", "Poe", 34, "pilot", "navigator",
                 "module_2", "dameron_poe@mars.org")
        add_user("Windu", "Mace", 43, "Jedi Masters", "teacher",
                 "module_3", "windu_mace@mars.org")

        # Первая работа
        add_job(1, "deployment of residential modules 1 and 2", 15, "2, 3",
                datetime.datetime.now(), False)
        add_job(2, "deployment of residential modules 2 and 3", 15, "1, 2",
                datetime.datetime.now(), False)
    # api v2 (flask-restful)
    # для списка объектов
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')

    app.run(port=8080, host='127.0.0.1')  # , debug=True)


if __name__ == '__main__':
    main()
