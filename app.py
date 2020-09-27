from flask import Flask, session, redirect, request
from flask import render_template as rt
import sqlite3
from flask import g
database = sqlite3.connect('example.db',
                           check_same_thread=False)  #columnas username, pass

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#primera vista de la pagina
@app.route('/')
def inicio():
    if sesionIniciada(): return rt("index.html", opcion="SALIR")
    else: return rt("index.html", opcion="INGRESO")


#menu novedades
@app.route("/novedades")
def novedades():
    return rt("novedades.html", opcion=getopcion())


#menu categorias
#madera
@app.route("/madera")
def madera():
    return rt("madera.html", opcion=getopcion())


#arcilla
@app.route("/arcilla")
def arcilla():
    return rt("arcilla.html", opcion=getopcion())


#tejido
@app.route("/tejido")
def tejido():
    return rt("tejido.html", opcion=getopcion())


#pintura
@app.route("/pintura")
def pintura():
    return rt("Pintura.html", opcion=getopcion())


#promociones
@app.route("/promociones")
def promociones():
    return rt("pricing.html", opcion=getopcion())


#sobre nosotros
@app.route("/nosotros")
def informacion():
    return rt("sobrenosotros.html", opcion=getopcion())


#contactanos
@app.route("/contactanos")
def contactanos():
    return rt("contactanos.html", opcion=getopcion())


#ingreso
@app.route("/ingreso")
def ingreso():
    if sesionIniciada():
        session.pop("username")
        return redirect("/")
    return rt("ingreso.html", opcion=getopcion())


#registro
@app.route("/registro")
def registro():
    return rt("registro.html", opcion=getopcion())


#


#chat
@app.route("/chat")
def chat():
    return rt("Chat.html", opcion=getopcion())


#inciarSesion
@app.route("/iniciarSesion", methods=["POST"])
def login():
    #solicitar usuario y contraseña del form en el forntend
    u = request.form["username"]  #usurio
    p = request.form["pass"]  #contra
    c = database.cursor()  #acceso a la base de datos
    c.execute("SELECT pass  from pass WHERE username=\'" + u + "\'" +
              " and pass=\'" + p +
              "\'")  #query a la base de tados para validar credenciales
    rows = c.fetchall()  #validar query
    if len(
            rows
    ):  #si la base de datos registar una respuesta positiva entonce se abrega al usuario a la session
        session['username'] = u
        return redirect('/')
    #si el usuario no esta en la base de datos se envia el error de credenciales incorrectas y se vuelve a solicitar el inreso de la credenciales
    return rt("ingreso.html", opcion=getopcion(
    )) + "<script>alert('usuario o contrasieña  incorrecta');</script>"


#verificar sesion
def sesionIniciada():
    return "username" in session


#solicitar estado actual del programa(si el usario a iniciado o no sesion)
def getopcion():
    if sesionIniciada():
        return "SALIR"
    return "INGRESO"


#Registrar usuarios en la base de datos
@app.route("/registrar", methods=["POST"])
def registrar():
    #solicitar usuario y contraseña del form en el forntend
    u = request.form["username"]  #usurio
    p = request.form["pass"]  #contra
    c = database.cursor()  #acceso a la base de datos
    c.execute(
        "SELECT pass  from pass WHERE username=\'" + u + "\'"
    )  #query a la base de tados para validar que el usurio que se intenta registrar no exista
    rows = c.fetchall()  #validar query
    if len(
            rows
    ) == 0:  #si la base de datos devuelve un valor nulo es decir que el usuario ne existe entonces este se agrega a la base de datos y se inicia sesion directamente
        #introducir usuario a la base de datos
        c.execute("INSERT INTO pass VALUES(\'" + u + "\',\'" + p + "\')")
        database.commit()
        #introducir usuario a la  sesion
        session['username'] = u
        return redirect('/')
    #si el usuario ya esta en la base de datos se avisas que ya esta registrado y no se permite registrar correos repetidos
    return rt("registro.html", opcion=getopcion(
    )) + "<script>alert('correo  ya registrado intente nuevamente');</script>"


app.run(debug=True)
