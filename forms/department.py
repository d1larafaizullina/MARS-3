from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = IntegerField('Руководитель', validators=[DataRequired()])
    members = StringField('участники')
    email = StringField('email департамента')
    submit = SubmitField('Сохранить')
