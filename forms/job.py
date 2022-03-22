from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, IntegerField, DateField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField('Руководитель', validators=[DataRequired()])
    job = TextAreaField("Описание работы", validators=[DataRequired()])
    work_size = IntegerField('Объем работы в часах', validators=[DataRequired()])
    collaborators = StringField('Список id участников', validators=[DataRequired()])
    start_date = DateField("Дата начала")
    end_date = DateField("Дата окончания")
    is_finished = BooleanField("Признак завершения", default=False)
    submit = SubmitField('Сохранить')
