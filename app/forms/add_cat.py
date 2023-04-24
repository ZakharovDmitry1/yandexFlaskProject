from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


def custom_validator(form, field):
    if len(field.data) < 5:
        raise validators.ValidationError('Input must be at least 5 characters long')


with open('cats_infotm/breed_cats.txt', 'r', encoding='utf-8') as readfile:
    list_of_breed2: list = readfile.read().split('\n')


class AddCat(FlaskForm):
    list_of_breed = list_of_breed2
    type_advertisement = StringField('Тип объявления', validators=[AnyOf(['for sale', 'in good hands', 'lost'])])
    breed = RadioField('Порода', validators=[AnyOf(list_of_breed)])
    title = StringField('Название объявления', validators=[DataRequired()], default='')
    description = StringField('Описание объявления', default='')
    pet_color = StringField('Окрас питомца', validators=[AnyOf(['белый', "черный", "рыжий", 'другой'])])
    cost = IntegerField('Цена питомца', default=0)
    telephone = StringField('Номер телефона')
    submit = SubmitField('Опубликовать')
