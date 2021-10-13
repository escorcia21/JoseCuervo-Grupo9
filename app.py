from flask import Flask, render_template

app = Flask(__name__)


# inicios de session y contraseña
@app.route('/', methods=["POST","GET"])
def login():
    '''
    En esta ruta se podra ingresar sesion siempre y cuando el usuario ya este 
    previamente registrado en la base de datos igualmente se podra recuperar la contraseña, guardar informacion o ver la politica de privacidad de datos
    '''
    return render_template("login.html")

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
@app.route('/dashboard', methods=["GET","DELETE"])
def dashboard():
    '''
    Este sera el dashboard tanto para superAdmins como para administradores en el se podra buscar, visualizar y añadir usuarios o empleados dependiendo del usuario que este usando la ap tambien se podra calificarlos, editarlos o eliminarlos.
    '''
    return render_template("dashboard.html")

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
    return render_template("registroSuper.html",titulo="Formulario de registro")

@app.route('/actualizar/usuario', methods=["PUT","GET"])
def actualizar_usuario():
    '''
    En esta ruta se podran actualizar usuarios a la base de datos, se debe diligenciar los campos que se desean actualizar. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''
    return render_template("registroSuper.html",titulo="Actualizar usuario")

@app.route('/calificar', methods=["POST","GET","PUT"])
def calificar():
    '''
    En esta ruta se podran agregar calificacion o editar ya existentes , ademas se debe ingresar la fecha y un pequeño comentario con no mas de 100 palabras. Se podra cancelar con el boton devolver el cual nos regresa al dashboard
    '''
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

if __name__ == "__main__":
    app.run(debug=True)