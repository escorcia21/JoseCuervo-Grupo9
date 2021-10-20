from flask import Flask, render_template,request, session,flash
import os

# base de datos
import sqlite3
from sqlite3 import Error

#seguridad
from markupsafe import escape
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = os.urandom( 24 )

roles = {1:"SUPERADMINISTRADOR",2:"ADMINISTRADOR",3:"EMPLEADO"}
disponible = {1:"disponible",0:"no disponible"}
activo = {1:"activo",0:"no activo"}


# inicios de session y contraseña
@app.route('/', methods=["POST","GET"])
def login():
    '''
    En esta ruta se podra ingresar sesion siempre y cuando el usuario ya este 
    previamente registrado en la base de datos igualmente se podra recuperar la contraseña, guardar informacion o ver la politica de privacidad de datos
    '''
    if "usuario" in  session:
        return redirect("dashboard")
    else:
        if request.method == "GET":
            return render_template("login.html")

        if request.method == "POST":
            usuario = escape(request.form["form-usuario"])
            contraseña = escape(request.form["form-contraseña"])

            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    cur = con.cursor()
                    cur.execute("SELECT contraseña,rol,nombre,apellido,email FROM usuario WHERE CC = ?", [usuario])
                    row = cur.fetchone()
                    if row is None:
                        flash("Usuario no encontrado")
                        return render_template("login.html")
                    else:
                        clavehash = row[0]
                        if check_password_hash(clavehash,contraseña):
                            session["usuario"] = usuario 
                            session["rol"] = row[1]
                            session["nombre"] = row[2]
                            session["apellido"] = row[3]
                            session["email"] = row[4]
                            if (int(row[1]) == 1 or int(row[1]) == 2):
                                return redirect("dashboard")
                            elif (int(row[1]) == 3):
                                return redirect("empleado")
                        else:
                            flash("Contraseña invalida")
                            return render_template("login.html")
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
       

@app.route('/recuperar', methods=["POST","GET"])
def recuperar():
    '''
    En esta ruta se ingresaran las credenciales (cedula y correo) para asi poder recuperar tu contraseña estas credenciales se comprobaran y si estan correctas se le enviara un correo al solicitante con un nuevo link en el se le abrira otra pagina, en la cual este podra ingresar su nueva contraseña y confirmarla
    '''
    return render_template("recuperar.html")

@app.route('/restablecer', methods=["POST","GET"])
def restablecer():
    '''
    este esta ruta se podra ingresar su nueva contraseña y confirmarla acto seguido se cambiara la contraseña del usuario en la base de datos

    NOTA: esta vista solo se podra ver una vez enviado el link para el cambio de contraseña via correo
    '''
    return render_template("restablecer.html")


#vistas de administradores
@app.route('/dashboard', methods=["GET","PUT"])
def dashboard():
    '''
    Este sera el dashboard tanto para superAdmins como para administradores en el se podra buscar, visualizar y añadir usuarios o empleados dependiendo del usuario que este usando la ap tambien se podra calificarlos, editarlos o eliminarlos.
    '''
    if "usuario" in session:

        rol = roles[session["rol"]]
        target = "USUARIOS"
        if session["rol"] == 2:
            target = "EMPLEADOS"

        if request.method == "GET":
            # obtener todos los usuarios de la base de datos
            nombres = session["nombre"] + " " + session["apellido"]
            nombres = nombres.upper()

            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT CC,nombre,foto,apellido FROM usuario")
                    row = cur.fetchall()
                    print(row)
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))

            return render_template("dashboard.html",nombre=nombres, rol=rol,target=target, row = row,Unombre="Nombre",cedula="Cedula",ocupacion="Ocupación")

        if request.method == "PUT":
            return render_template("dashboard.html",nombre=session["nombre"], rol=rol)
    else:
        return redirect("/")

@app.route('/registro', methods=["POST","GET"])
def registroAdmin():
    '''
    En esta ruta se podran agregar empleados a la base de datos, se debe diligenciar todo el formulario  a excepcion de la foto de peril, esta sera opcional. Se podra cancelar el registro con el boton devolver el cual nos regresa al dashboard
    '''
    return render_template("registroAdmin.html", titulo="Formulario de registro")

@app.route('/actualizar/empleado', methods=["PUT","GET"])
def actualizar_empleado():
    '''
    En esta ruta se podran actualizar empleados a la base de datos, se debe diligenciar los campos que se desean actualizar. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''
    return render_template("registroAdmin.html", titulo="Actualizar empleado")

@app.route('/registroSuper', methods=["POST","GET"])
def registroSuper():
    '''
    En esta ruta se podran actualizar usuarios a la base de datos, se debe diligenciar los campos que se desean actualizar, tambien se podra asignar un rol. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''
    if "usuario" in  session:
        if request.method == "GET":
            return render_template("registroSuper.html",titulo="Formulario de registro")

        if request.method == "POST":
            nombre = escape(request.form["nombre"])
            nacimiento = escape(request.form["nacimiento"])
            estado_civil = escape(request.form["estado_civil"])
            apellido = escape(request.form["apellido"])
            edad = escape(request.form["edad"])
            email = escape(request.form["email"])
            cedula = escape(request.form["cedula"])
            celular = escape(request.form["celular"])
            direccion = escape(request.form["direccion"])
            ingreso = escape(request.form["ingreso"])
            cargo = escape(request.form["cargo"])
            termino = escape(request.form["termino"])
            salario = escape(request.form["salario"])
            tipo = escape(request.form["tipo"])
            disponibilidad = escape(request.form["disponibilidad"])
            rol = escape(request.form["select"])
            foto = escape(request.form["upload"])

            if disponibilidad.lower() == "disponible":
                disponibilidad = 1
            elif disponibilidad.lower() == "no disponible":
                disponibilidad = 0
                
            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO usuario (CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,contraseña,activo,primera_vez,registrador,apellido,fecha_nacimiento,cargo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (cedula,nombre,edad,estado_civil,celular,direccion,email,ingreso,termino,tipo,salario,rol,disponibilidad,foto,cedula,1,1,session["email"],apellido,nacimiento,cargo))
                    con.commit()
            except Error as er:
                flash("Ocurrio un error")
                print('SQLite error: %s' % (' '.join(er.args)))
            return redirect('/registroSuper')
    else:
        return redirect("/")

        
    

@app.route('/actualizar/<int:cedula>', methods=["POST","GET"])
def actualizar_usuario(cedula):
    '''
    En esta ruta se podran actualizar usuarios a la base de datos, se debe diligenciar los campos que se desean actualizar. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''

    if "usuario" in session:
        rol = roles[session["rol"]]
        nombres = session["nombre"] + " " + session["apellido"]
        nombres = nombres.upper()
        if request.method == "GET":
            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,apellido,fecha_nacimiento,cargo FROM usuario WHERE CC=?",[str(cedula)])
                    usuario = cur.fetchone()

                    if usuario is None:
                        return redirect(f"/dashboard/{cedula}")
                    else:
                        return render_template("registroSuper.html",nombre=nombres, rol=rol,Unombre=usuario["nombre"],apellido=usuario["apellido"],edad=usuario["edad"],cargo=usuario["cargo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"],ingreso=usuario["fecha_ingreso"],termino=usuario["fecha_termino"],tipo=usuario["tipo_contrato"],salario=usuario["salario"],Rol=usuario["rol"],disponible=disponible[usuario["disponibilidad"]])
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
        
        if request.method == "POST":
            nombre = escape(request.form["nombre"])
            nacimiento = escape(request.form["nacimiento"])
            estado_civil = escape(request.form["estado_civil"])
            apellido = escape(request.form["apellido"])
            edad = escape(request.form["edad"])
            email = escape(request.form["email"])
            #ucedula = escape(request.form["cedula"])
            celular = escape(request.form["celular"])
            direccion = escape(request.form["direccion"])
            ingreso = escape(request.form["ingreso"])
            cargo = escape(request.form["cargo"])
            termino = escape(request.form["termino"])
            salario = escape(request.form["salario"])
            tipo = escape(request.form["tipo"])
            udisponibilidad = escape(request.form["disponibilidad"])
            urol = escape(request.form["select"])
            foto = escape(request.form["upload"])

            if udisponibilidad.lower() == "disponible":
                udisponibilidad = 1
            elif udisponibilidad.lower() == "no disponible":
                udisponibilidad = 0

            try :
                with sqlite3.connect('joseCuervoDB.db') as con:
                    cur = con.cursor()
                    cur.execute('UPDATE usuario SET nombre=?,edad=?,estado_civil=?,celular=?,direccion=?,email=?,fecha_ingreso=?,fecha_termino=?,tipo_contrato=?,salario=?,rol=?,disponibilidad=?,foto=?,apellido=?,fecha_nacimiento=?,cargo=? WHERE CC=?',(nombre,edad,estado_civil,celular,direccion,email,ingreso,termino,tipo,salario,urol,udisponibilidad,foto,apellido,nacimiento,cargo,cedula))
                    con.commit()
                    if con.total_changes > 0:
                        flash("Actualizado con exito")
                        return redirect(f"/dashboard/{cedula}")
                    else:
                        flash("Ocurrio un error")
                        return redirect(f"/actualizar/{cedula}")
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
    else:
        return redirect("/")

@app.route('/calificar/<int:cedula>', methods=["POST","GET","PUT"])
def calificar(cedula):
    '''
    En esta ruta se podran agregar calificacion o editar ya existentes , ademas se debe ingresar la fecha y un pequeño comentario con no mas de 100 palabras. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''
    # INSERT INTO calificaciones_usuario (calificacion,usuario,evaluador,fecha) VALUES (?,?,?,?)
    return render_template("vistacalificar.html")


# vistas de empleado
@app.route('/empleado', methods=["GET"])
def empleado():
    '''
    En esta ruta pertenece al usuario de tipo empleado
    en esta podra consultar toda su informacion personal, ademas podra generar una peticion de actualizacion de datos.
    '''
    return render_template("vistaEmpleado.html")

@app.route('/solicitud', methods=["PUT","GET"])
def solicitud():
    '''
    En esta ruta pertenece a la peticion de actualizacion de datos, se debe diligenciar el formulario para asi ser enviado via correo al usuario que registro a dicho empleado. Se podra cancelar con el boton devolver el cual nos regresa al dashboard de tipo empleado.
    '''
    return render_template("solicitud.html")


#politicas
@app.route('/politicas',methods=["GET"])
def politicas():
    '''
    En esta ruta se podra ver la politica de tratamiento de datos y terminos y condiciones.
    '''
    return render_template("politicas.html")

@app.route("/dashboard/<int:cedula>", methods=['GET'])
def buscar(cedula):
    if "usuario" in session:
        # print(request.path.split('/')[2])
        rol = roles[session["rol"]]
        target = "USUARIOS"
        if session["rol"] == 2:
            target = "EMPLEADOS"

        if request.method == "GET":
            # obtener todos los usuarios de la base de datos
            nombres = session["nombre"] + " " + session["apellido"]
            nombres = nombres.upper()

            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,apellido,fecha_nacimiento,cargo FROM usuario WHERE CC=?",[str(cedula)])
                    usuario = cur.fetchone()

                    cur.execute("SELECT CC,nombre,foto,apellido FROM usuario")
                    row = cur.fetchall()

                    if usuario is None:
                        return redirect("/dashboard")
                    else:
                        return render_template("dashboard.html",nombre=nombres, rol=rol,target=target, row = row, Unombre=usuario["nombre"],edad=usuario["edad"],ocupacion=usuario["cargo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"],ingreso=usuario["fecha_ingreso"],termino=usuario["fecha_termino"],tipo=usuario["tipo_contrato"],salario=usuario["salario"],Rol=roles[usuario["rol"]].lower(),disponible=disponible[usuario["disponibilidad"]])
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
    else:
        return redirect("/")


@app.route('/logout')
def logout():
    if "usuario" in session:
        session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)