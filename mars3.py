import datetime

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from forms.loginform import LoginForm
from forms.user import RegisterForm
from forms.job import JobsForm
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/jobs")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()  # filter(News.is_private != True)
    return render_template("jobs.html", jobs=jobs)


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
             address, email, password="P@ssw0rd"):
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


def add_job(team_leader, job_, work_size,
            collaborators, start_date, is_finished):
    job = Jobs(
        team_leader=team_leader,
        job=job_,
        work_size=work_size,
        collaborators=collaborators,
        start_date=start_date,
        is_finished=is_finished
    )
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
    add_job(1, "deployment of residential modules 1 and 2", 15, "2, 3",
            datetime.datetime.now(), False)
    add_job(2, "deployment of residential modules 2 and 3", 15, "1, 2",
            datetime.datetime.now(), False)

    app.run(port=8080, host='127.0.0.1')  # , debug=True)


if __name__ == '__main__':
    main()
