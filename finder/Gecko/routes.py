from Gecko import app, db
from Gecko.models import Usuario, Price
from Gecko.forms import RegisterForm, LoginForm, UrlForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, session, flash, redirect, url_for, request
from Gecko.funcs import getPrice


# Routes

# Errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.route("/", methods=["GET", "POST"])
def home_page():
    form = UrlForm()

    if request.method == "POST":
        price = getPrice(form.url.data)
        if price == False:
            flash(f"Sorry, price not found", category="danger")
        else:
            flash(f"Buy for: {price}$ ARS", category="success")
    return render_template("/home.html", form=form)

@app.route("/login.html", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user_to_login = Usuario.query.filter_by(email=form.email.data).first()
        if user_to_login and user_to_login.check_password(password=form.password.data):
            login_user(user_to_login)
            flash(f"¡Hi {user_to_login.nombre}, nice to see you back!", category="success")
            session.permanent = True
            return redirect(url_for("profile_page"))
        else:
            flash("Sorry, your email or password was incorrect. Please double-check it.", category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"{err_msg}", category="danger")
    return render_template("/login.html", form=form)

@app.route("/logout.html")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))

@app.route("/register.html", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()

    if request.method == "POST":
        username_to_login = Usuario.query.filter_by(username=form.username.data).first()
        email_to_login = Usuario.query.filter_by(email=form.email.data).first()
        if username_to_login:
            flash(f"Username: '{form.username.data}' already exists.", category="danger")
        if email_to_login:
            flash(f"Email: '{form.email.data}' is already in use.", category="danger")
        else:
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

@app.route("/profile.html", methods=["GET", "POST"])
def profile_page():
    if request.method == "GET":
        user = Usuario.query.filter_by(id=current_user.id)
        return render_template("/profile.html", user=user)

@app.route("/dashboard.html", methods=["GET", "POST"])
def dashboard_page():
    if request.method == "GET":
        data = Price.query.filter_by(usuario_id=current_user.id)
        return render_template("/dashboard.html", data=data)