from flask import Flask, render_template, make_response, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from app.data.users import User
from app.forms.add_cat import AddCat
from app.forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")
db_sess = db_session.create_session()

db_sess.commit()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'это страница не найдена'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'некорректный запрос или ошибка в запросе'}), 400)

@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('main_window.html')

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
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.email = form.email.data
        user.position = form.position.data
        user.age = form.age.data
        user.address = form.address.data
        user.speciality = form.speciality.data
        user.set_password(form.password.data)
        print(user)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
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

@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    form = AddCat()
    if form.validate_on_submit():
        db_sess.commit()
        return redirect('/')
    return render_template('add_cat.html', form=form)



def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()

