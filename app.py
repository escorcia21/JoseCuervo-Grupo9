from logging import error
from flask import Flask, render_template,request, session,flash
from flask_mail import Mail,Message
import os

# base de datos
import sqlite3
from sqlite3 import Error

#seguridad
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect, secure_filename


UPLOAD_FOLDER = 'static\profile'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom( 24 )
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'josecuerv302@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mintic2022*'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

roles = {1:"SUPERADMINISTRADOR",2:"ADMINISTRADOR",3:"EMPLEADO"}
disponible = {1:"activo",0:"no activo"}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
                    cur.execute("SELECT contraseña,rol,nombre,apellido,email,foto FROM usuario WHERE CC = ? AND disponibilidad=?", [usuario,1])
                    row = cur.fetchone()
                    if row is None:
                        flash("Usuario no encontrado","error")
                        return render_template("login.html")
                    else:
                        clavehash = row[0]
                        if check_password_hash(clavehash,contraseña):
                            session["usuario"] = usuario 
                            session["rol"] = row[1]
                            session["nombre"] = row[2]
                            session["apellido"] = row[3]
                            session["email"] = row[4]
                            session["foto"] = row[5]
                            if (int(row[1]) == 1 or int(row[1]) == 2):
                                return redirect("dashboard")
                            else:
                                return redirect("empleado")
                        else:
                            flash("Contraseña invalida","error")
                            return render_template("login.html")
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                return render_template("login.html")
       
# @app.route('/recuperar', methods=["POST","GET"])
# def recuperar():
#     '''
#     En esta ruta se ingresaran las credenciales (cedula y correo) para asi poder recuperar tu contraseña estas credenciales se comprobaran y si estan correctas se le enviara un correo al solicitante con un nuevo link en el se le abrira otra pagina, en la cual este podra ingresar su nueva contraseña y confirmarla
#     '''
    
#     if request.method == "GET": 
#         return render_template("recuperar.html")


#     if request.method == "POST":
#         cedula = escape(request.form["cedula"])
#         email = escape(request.form["email"])
        
#         try:
#             with sqlite3.connect('joseCuervoDB.db') as con:
#                 con.row_factory = sqlite3.Row 
#                 cur = con.cursor()
#                 cur.execute("SELECT CC,email  FROM usuario WHERE CC=? AND disponibilidad=? AND email=?",[str(cedula),1,email])
#                 usuario = cur.fetchone()

#                 if usuario is None:
#                     flash("Credenciales invalidas","error")
#                     return redirect("/")
#                 else:
#                     yag = yagmail.SMTP('josecuerv302', 'Mintic2022*') 
#                     yag.send(to =email , subject = "Activa tu cuenta", contents = "Bienvenido, ingresa al siguiente link: http://127.0.0.1:5000/recuperar cuenta")
#                     flash("Revisa tu correo para activar","info")
#                     return redirect("/")
#         except Exception as er:
#             print(er)
#             return redirect("/")

@app.route('/restablecer', methods=["POST","GET"])
def restablecer():
    '''
    este esta ruta se podra ingresar su nueva contraseña y confirmarla acto seguido se cambiara la contraseña del usuario en la base de datos

    NOTA: esta vista solo se podra ver una vez enviado el link para el cambio de contraseña via correo
    '''
    if "usuario" in session:
        if request.method == "GET":
            return render_template("restablecer.html")

        if request.method == "POST":
            return redirect("/restablecer")
    else:
        return redirect("/")

#vistas de administradores
@app.route('/dashboard', methods=["GET","POST"])
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

            if session["rol"] != 3:
                # obtener todos los usuarios de la base de datos
                nombres = session["nombre"] + " " + session["apellido"]
                nombres = nombres.upper()
                imagen = "imgs/default.png"
                try:
                    with sqlite3.connect('joseCuervoDB.db') as con:
                        con.row_factory = sqlite3.Row 
                        cur = con.cursor()
                        if session["rol"] == 2:
                            cur.execute("SELECT CC,nombre,foto,apellido FROM usuario WHERE CC != ? AND rol = ? AND disponibilidad=?",[session["usuario"],3,1])
                        else: 
                            cur.execute("SELECT CC,nombre,foto,apellido FROM usuario WHERE CC != ? AND disponibilidad=?",[session["usuario"],1])
                            
                        row = cur.fetchall()
                except Error  as er:
                    print('SQLite error: %s' % (' '.join(er.args)))

                return render_template("dashboard.html",nombre=nombres, rol=rol,target=target, row = row,Unombre="Nombre",cedula="Cedula",sexo="Sexo",imagen=imagen,perfil=session["foto"])
            else:
                return redirect("/empleado")

        if request.method == "POST":
            cedula = escape(request.form["disponibilidad__cedula"])

            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    if session["rol"] == 1:
                        cur.execute("UPDATE usuario SET disponibilidad=?  WHERE CC=?",[0,cedula])
                    else:
                        cur.execute("UPDATE usuario SET disponibilidad=?  WHERE CC=? AND rol=?",[0,cedula,3])
                    con.commit()
                    if con.total_changes > 0:
                        flash("Eliminado con exito","info")
                        return redirect("/dashboard")
                    else:
                        flash("No se pudo eliminar","error")
                        return redirect("/dashboard")
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                return redirect("/dashboard")
    else:
        return redirect("/")

@app.route('/registro', methods=["POST","GET"])
def registro():
    '''
    En esta ruta se podran actualizar usuarios a la base de datos, se debe diligenciar los campos que se desean actualizar, tambien se podra asignar un rol. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''
    if "usuario" in  session:
        rol = roles[session["rol"]]
        nombres = session["nombre"] + " " + session["apellido"]
        nombres = nombres.upper()
        
        if request.method == "GET":
            if session["rol"] == 1:
                return render_template("registroSuper.html",titulo="Formulario de registro",nombre=nombres, rol=rol,perfil=session["foto"])
            elif session["rol"] == 2:
                return render_template("registroAdmin.html",titulo="Formulario de registro",nombre=nombres, rol=rol,perfil=session["foto"])
            else:
                return redirect("/empleado")

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
            sexo = escape(request.form["sexo"])
            termino = escape(request.form["termino"])
            salario = escape(request.form["salario"])
            tipo = escape(request.form["tipo"])
            disponibilidad = escape(request.form["disponibilidad"])
            if session["rol"] == 2:
                rol = 3
            else:
                rol = escape(request.form["select"])
            #foto = escape(request.form["upload"])
            cedulahash = generate_password_hash(cedula)

            file = request.files['archivo']
            filename = secure_filename(file.filename)
            if filename=="":
                filename="profile/default.png"
            elif file and allowed_file(filename):
                filename = filename.rsplit('.', 1)
                filename[0] = str(cedula)
                filename = filename[0]+"."+filename[1]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = "profile/"+filename
            else:
                flash("No se subio la foto, extension no soportada","error")


            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO usuario (CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,contraseña,primera_vez,registrador,apellido,fecha_nacimiento,sexo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (cedula,nombre,edad,estado_civil,celular,direccion,email,ingreso,termino,tipo,salario,rol,disponibilidad,filename,cedulahash,1,session["email"],apellido,nacimiento,sexo))
                    con.commit()
                    flash("Registrado con exito","info")
                    return redirect('/dashboard')
            except Error as er:
                flash("Ocurrio un error","error")
                print('SQLite error: %s' % (' '.join(er.args)))
                return redirect('/registro')
        
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
                    cur.execute("SELECT CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,apellido,fecha_nacimiento,sexo FROM usuario WHERE CC=? AND disponibilidad=?",[str(cedula),1])
                    usuario = cur.fetchone()

                    if usuario is None:
                        return redirect(f"/dashboard/{cedula}")
                    else:
                        if session["rol"] == 1:
                            return render_template("registroSuper.html",nombre=nombres, rol=rol,Unombre=usuario["nombre"],apellido=usuario["apellido"],edad=usuario["edad"],sexo=usuario["sexo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"],ingreso=usuario["fecha_ingreso"],termino=usuario["fecha_termino"],salario=usuario["salario"],Rol=usuario["rol"],disponible=disponible[usuario["disponibilidad"]],perfil=session["foto"])
                        if session["rol"] == 2:
                            return render_template("registroAdmin.html",nombre=nombres,Unombre=usuario["nombre"],apellido=usuario["apellido"],edad=usuario["edad"],sexo=usuario["sexo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"],ingreso=usuario["fecha_ingreso"],termino=usuario["fecha_termino"],salario=usuario["salario"], rol=rol,disponible=disponible[usuario["disponibilidad"]],perfil=session["foto"])
                        else:
                            return redirect("/empleado")
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))

        
        if request.method == "POST":
            nombre = escape(request.form["nombre"])
            nacimiento = escape(request.form["nacimiento"])
            estado_civil = escape(request.form["estado_civil"])
            apellido = escape(request.form["apellido"])
            edad = escape(request.form["edad"])
            email = escape(request.form["email"])
            celular = escape(request.form["celular"])
            direccion = escape(request.form["direccion"])
            ingreso = escape(request.form["ingreso"])
            sexo = escape(request.form["sexo"])
            termino = escape(request.form["termino"])
            salario = escape(request.form["salario"])
            tipo = escape(request.form["tipo"])
            udisponibilidad = escape(request.form["disponibilidad"])
            if session["rol"] == 1:
                urol = escape(request.form["select"])
            else:
                urol = 3

            
            file = request.files['archivo']
            filename = secure_filename(file.filename)
            if filename=="":
                filename="profile/default.png"
            elif file and allowed_file(filename):
                filename = filename.rsplit('.', 1)
                filename[0] = str(cedula)
                filename = filename[0]+"."+filename[1]
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = "profile/"+filename
            else:
                flash("No se subio la foto, extension no soportada","error")


            try :
                with sqlite3.connect('joseCuervoDB.db') as con:
                    cur = con.cursor()
                    cur.execute('UPDATE usuario SET nombre=?,edad=?,estado_civil=?,celular=?,direccion=?,email=?,fecha_ingreso=?,fecha_termino=?,tipo_contrato=?,salario=?,rol=?,disponibilidad=?,foto=?,apellido=?,fecha_nacimiento=?,sexo=? WHERE CC=?',(nombre,edad,estado_civil,celular,direccion,email,ingreso,termino,tipo,salario,urol,udisponibilidad,filename,apellido,nacimiento,sexo,cedula))
                    con.commit()
                    if con.total_changes > 0:
                        flash("Actualizado con exito","info")
                        return redirect(f"/dashboard/{cedula}")
                    else:
                        flash("Ocurrio un error","error")
                        return redirect(f"/actualizar/{cedula}")
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                return redirect(f"/actualizar/{cedula}")
    else:
        return redirect("/")

@app.route('/calificar/<int:cedula>', methods=["POST","GET"])
def calificar(cedula):
    '''
    En esta ruta se podran agregar calificacion o editar ya existentes , ademas se debe ingresar la fecha y un pequeño comentario con no mas de 100 palabras. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''
    # INSERT INTO calificaciones_usuario (calificacion,usuario,evaluador,fecha) VALUES (?,?,?,?)

    if "usuario" in session and cedula != int(session["usuario"]):
        rol = roles[session["rol"]]
        nombres = session["nombre"] + " " + session["apellido"]
        nombres = nombres.upper()

        if request.method == "GET":
            if session["rol"] != 3:
                try:
                    with sqlite3.connect('joseCuervoDB.db') as con:
                        con.row_factory = sqlite3.Row 
                        cur = con.cursor()
                        
                        if session["rol"] == 3:
                            cur.execute("SELECT CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,apellido,fecha_nacimiento,sexo FROM usuario WHERE CC=? AND rol=? AND disponibilidad=?",(str(cedula),3,1))
                            usuario = cur.fetchone()
                        else: 
                            cur.execute("SELECT CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,apellido,fecha_nacimiento,sexo FROM usuario WHERE CC=?  AND disponibilidad=?",[str(cedula),1])
                            usuario = cur.fetchone()

                        if usuario is None:
                            return redirect("/dashboard")
                        else:
                            cur.execute("SELECT comentario,fecha,calificacion FROM calificaciones_usuario WHERE usuario=?",[str(cedula)])
                            calificaciones = cur.fetchall()

                            return render_template("vistacalificar.html",nombre=nombres, rol=rol,Unombre=usuario["nombre"],apellido=usuario["apellido"],edad=usuario["edad"],sexo=usuario["sexo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"],ingreso=usuario["fecha_ingreso"],termino=usuario["fecha_termino"],tipo=usuario["tipo_contrato"],salario=usuario["salario"],cargo=roles[usuario["rol"]].lower(),disponible=disponible[usuario["disponibilidad"]],cali=calificaciones,imagen=usuario["foto"],perfil=session["foto"])
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    return redirect(f"/dashboard/{cedula}")
            else:
                return redirect("/empleado")

        if request.method == "POST":
            calificacion = escape(request.form["Ccalificacion"])
            fecha = escape(request.form["fcalificacion"])
            comentario = escape(request.form["comentario"])

            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("INSERT INTO calificaciones_usuario (calificacion,usuario,evaluador,fecha,comentario) VALUES (?,?,?,?,?)",(calificacion,str(cedula),session["usuario"],fecha,comentario))
                    con.commit()
                    flash("Calificación agregado con exito","info")
            except Error as er:
                flash("Calificación un error al agregar un mensaje","error")
                print('SQLite error: %s' % (' '.join(er.args)))

            return redirect(f"/calificar/{cedula}")
    else:
        return redirect("/")

# vistas de empleado
@app.route('/empleado', methods=["GET"])
def empleado():
    '''
    En esta ruta pertenece al usuario de tipo empleado
    en esta podra consultar toda su informacion personal, ademas podra generar una peticion de actualizacion de datos.
    '''
    if "usuario" in  session and session["rol"] == 3:
        rol = roles[session["rol"]]
        nombres = session["nombre"] + " " + session["apellido"]
        nombres = nombres.upper()
    
        if request.method == "GET":
            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    
                    if session["rol"] == 3:
                        cur.execute("SELECT CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,apellido,fecha_nacimiento,sexo FROM usuario WHERE CC=? AND disponibilidad=?" ,[str(session["usuario"]),1])
                        usuario = cur.fetchone()
                    
                        if usuario is None:
                            return redirect("/login")
                        else:
                            cur.execute("SELECT comentario,fecha,calificacion FROM calificaciones_usuario WHERE usuario=?",[str(session["usuario"])])
                            calificaciones = cur.fetchall()

                            return render_template("vistaEmpleado.html",nombre=nombres, rol=rol,Unombre=usuario["nombre"],apellido=usuario["apellido"],edad=usuario["edad"],sexo=usuario["sexo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"],ingreso=usuario["fecha_ingreso"],termino=usuario["fecha_termino"],tipo=usuario["tipo_contrato"],salario=usuario["salario"],cargo=roles[usuario["rol"]].lower(),disponible=disponible[usuario["disponibilidad"]],cali=calificaciones,imagen=usuario["foto"],perfil=session["foto"])
                    else :
                        return redirect("/")
                    
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                return redirect("/")
        else:
            return redirect("/empleado")
    else:
        return redirect("/")

@app.route('/solicitud', methods=["POST","GET"])
def solicitud():
    '''
    En esta ruta pertenece a la peticion de actualizacion de datos, se debe diligenciar el formulario para asi ser enviado via correo al usuario que registro a dicho empleado. Se podra cancelar con el boton devolver el cual nos regresa al dashboard de tipo empleado.
    '''
    if "usuario" in session and session["rol"] == 3:
        nombres = session["nombre"] + " " + session["apellido"]
        nombres = nombres.upper()

        
        with sqlite3.connect('joseCuervoDB.db') as con:
            con.row_factory = sqlite3.Row 
            cur = con.cursor()
            cur.execute("SELECT CC,nombre,apellido,edad,estado_civil,celular,direccion,email,fecha_nacimiento,sexo FROM usuario WHERE CC=?",[str(session["usuario"])])
            usuario = cur.fetchone()

            if usuario is None:
                return redirect("/solicitud")
            else:
                formulario = render_template("solicitud.html",perfil=session["foto"],nombre=nombres,rol=roles[session["rol"]],Unombre=usuario["nombre"],apellido=usuario["apellido"],edad=usuario["edad"],sexo=usuario["sexo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"])

                if request.method == "GET":
                    return formulario

                if request.method == "POST":
                    nombre = escape(request.form["nombre"])
                    nacimiento = escape(request.form["nacimiento"])
                    estado_civil = escape(request.form["estado_civil"])
                    apellido = escape(request.form["apellido"])
                    edad = escape(request.form["edad"])
                    email = escape(request.form["email"])
                    cedula = escape(session["usuario"])
                    celular = escape(request.form["celular"])
                    direccion = escape(request.form["direccion"])
                    sexo = escape(request.form["sexo"])
                    cometarios = escape(request.form["cometarios"])
                    msg = Message('Peticion de actualizacion de datos', sender = app.config['MAIL_USERNAME'], recipients = [session["email"]])
                    msg.body = f"Nombre: {nombre} Apellido: {apellido} Edad: {edad}\nNacimiento: {nacimiento} Email: {email} Celular: {celular}\nCedula: {cedula} Dirección: {direccion} Estado civil: {estado_civil}\nSexo: {sexo}\n\nComentarios:\n{cometarios}"
                    mail.send(msg)
                    flash("Mensaje enviado con exito","info")
                    return redirect("/empleado")
    else:
        return redirect("/")

#politicas
@app.route('/politicas',methods=["GET"])
def politicas():
    '''
    En esta ruta se podra ver la politica de tratamiento de datos y terminos y condiciones.
    '''
    return render_template("politicas.html")

@app.route("/dashboard/<int:cedula>", methods=['GET',"POST"])
def buscar(cedula):
    if "usuario" in session:
        # print(request.path.split('/')[2])
        rol = roles[session["rol"]]
        target = "USUARIOS"
        if session["rol"] == 2:
            target = "EMPLEADOS"

        if request.method == "POST":
            cedula = escape(request.form["disponibilidad__cedula"])

            try:
                with sqlite3.connect('joseCuervoDB.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    if session["rol"] == 1:
                        cur.execute("UPDATE usuario SET disponibilidad=?  WHERE CC=?",[0,cedula])
                    else:
                        cur.execute("UPDATE usuario SET disponibilidad=?  WHERE CC=? AND rol=?",[0,cedula,3])
                    con.commit()
                    if con.total_changes > 0:
                        flash("Eliminado con exito","info")
                        return redirect(f"/dashboard/{cedula}")
                    else:
                        flash("No se pudo eliminar","error")
                        return redirect(f"/dashboard/{cedula}")
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                return redirect("/dashboard")


        if request.method == "GET":

            if session["rol"] != 3:
                # obtener todos los usuarios de la base de datos
                nombres = session["nombre"] + " " + session["apellido"]
                nombres = nombres.upper()
                try:
                    with sqlite3.connect('joseCuervoDB.db') as con:
                        con.row_factory = sqlite3.Row 
                        cur = con.cursor()
                        cur.execute("SELECT CC,nombre,edad,estado_civil,celular,direccion,email,fecha_ingreso,fecha_termino,tipo_contrato,salario,rol,disponibilidad,foto,apellido,fecha_nacimiento,sexo FROM usuario WHERE CC=? AND disponibilidad=?",[str(cedula),1])
                        usuario = cur.fetchone()

                        if session["rol"] == 2:
                            cur.execute("SELECT CC,nombre,foto,apellido FROM usuario WHERE CC != ? AND rol = ? AND disponibilidad=?",[session["usuario"],3,1])
                        else: 
                            cur.execute("SELECT CC,nombre,foto,apellido FROM usuario WHERE CC != ? AND disponibilidad=?",[session["usuario"],1])

                        row = cur.fetchall()

                        if usuario is None:
                            return redirect("/dashboard")
                        else:
                            imagen = usuario["foto"]
                            return render_template("dashboard.html",nombre=nombres, rol=rol,target=target, row = row, Unombre=usuario["nombre"],edad=usuario["edad"],sexo=usuario["sexo"],cedula=usuario["CC"],nacimiento=usuario["fecha_nacimiento"],estado=usuario["estado_civil"],celular=usuario["celular"],direccion=usuario["direccion"],email=usuario["email"],ingreso=usuario["fecha_ingreso"],termino=usuario["fecha_termino"],tipo=usuario["tipo_contrato"],salario=usuario["salario"],Rol=roles[usuario["rol"]].lower(),disponible=disponible[usuario["disponibilidad"]],imagen=imagen,perfil=session["foto"])
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
            else:
                return redirect("/empleado")
    else:
        return redirect("/")

@app.route('/logout')
def logout():
    if "usuario" in session:
        session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)