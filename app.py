from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# TABLA USUARIOS
class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)

# TABLA CATEGORIAS
class Categoria(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

# CREAR BASE DE DATOS
with app.app_context():
    db.create_all()

# LOGIN
@app.route("/")
def login():
    return render_template("login.html")

# REGISTRO
@app.route("/register")
def register():
    return render_template("register.html")

# GUARDAR USUARIO
@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():

    username = request.form["username"]

    password = request.form["password"]

    nuevo_usuario = Usuario(
        username=username,
        password=password
    )

    db.session.add(nuevo_usuario)

    db.session.commit()

    return redirect("/")

# VALIDAR LOGIN
@app.route("/validar_login", methods=["POST"])
def validar_login():

    username = request.form["username"]

    password = request.form["password"]

    usuario = Usuario.query.filter_by(
        username=username,
        password=password
    ).first()

    if usuario:

        return redirect("/home")

    else:

        return "Usuario o contraseña incorrectos"

# CREAR CATEGORIA
@app.route("/crear_categoria", methods=["POST"])
def crear_categoria():

    nombre = request.form["nombre"]

    nueva_categoria = Categoria(
        nombre=nombre
    )

    db.session.add(nueva_categoria)

    db.session.commit()

    return redirect("/home")

# HOME
@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)