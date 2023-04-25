import secrets

from flask import render_template, redirect, make_response, jsonify, request
from flask_login import logout_user, login_required, login_manager, LoginManager, login_user

from app import app
from app.data import db_session
from app.data.posts import Posts
from app.data.users import User
from app.forms.add_cat import AddCat
from app.forms.user import RegisterForm, LoginForm

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'это страница не найдена'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'некорректный запрос или ошибка в запросе'}), 400)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def index():
    db_sess = db_session.create_session()
    posts = db_sess.query(Posts).all()
    return render_template('main2.html', posts=posts)

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
        print(User.email, form.email.data)
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
    db_sess = db_session.create_session()
    form = AddCat()
    if form.validate_on_submit():
        posts = Posts()
        posts.title = form.title.data
        posts.cost = form.cost.data
        try:
            f = request.files['file']
            if not f:
                raise Exception
            posts.image = secrets.token_hex(16) + '.png'
            with open(f'app/static/img/{posts.image}', 'wb') as file:
                file.write(f.read())
        except Exception:
            pass
        db_sess.add(posts)
        db_sess.commit()
        return redirect('/')
    return render_template('add_cat.html', form=form)