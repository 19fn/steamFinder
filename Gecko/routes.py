from Gecko import app, db
from Gecko.models import Usuario, Price
from Gecko.forms import RegisterForm, LoginForm, UrlForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, session, flash, redirect, url_for, request
from Gecko.funcs import getPrice


# Routes
@app.route("/")
@app.route("/home.html")
def home_page():
    return render_template("/home.html")

@app.route("/login.html", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user_to_login = Usuario.query.filter_by(email=form.email.data).first()
        if user_to_login and user_to_login.check_password(password=form.password.data):
            login_user(user_to_login)
            flash(f"¡Hi {user_to_login.nombre}, nice to see you back!", category="success")
            session.permanent = True
            return redirect(url_for("home_page"))
        else:
            flash("Correo Electronico o Contraseña Incorrecta.", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"{err_msg}", category="danger")
    return render_template("/login.html", form=form)

@app.route("/logout.html")
@login_required
def logout_page():
    logout_user()
    flash("Bye!",category="info")
    return redirect(url_for("home_page"))

@app.route("/register.html", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        crear_usuario = Usuario( nombre=form.nombre.data,
                                 username=form.username.data,
                                 email=form.email.data,
                                 passw=form.password.data )
        db.session.add(crear_usuario)
        db.session.commit()
        login_user(crear_usuario)
        flash(f"Se ha creado el usuario correctamente, Bienvenido/a {crear_usuario.nombre}!", category="success")
        session.permanent = True
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"{err_msg}", category="danger")
    return render_template("/register.html", form=form)

@app.route("/dashboard.html", methods=["GET", "POST"])
def dashboard_page():
    if request.method == "GET":
        data = Price.query.filter_by(usuario_id=current_user.id)
        return render_template("/dashboard.html", data=data)

@app.route("/search.html", methods=["GET", "POST"])
def search_page():
    form = UrlForm()

    if request.method == "POST":
        game_price = Price( game=form.game.data,
                            price=getPrice(form.url.data),
                            usuario_id=current_user.id )
        db.session.add(game_price)
        db.session.commit()
    return render_template("/search.html", form=form)