var a = document.getElementById("cc").disabled = true;
const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const textarea = document.getElementById('comentarios-area');

const expresiones = {
	//usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	comentarios: /^[a-zA-ZÀ-ÿ\s]{1,150}$/, // Letras y espacios, pueden llevar acentos.
	numeros: /^.{4,120}$/, // 4 a 12 digitos.
	direccion: /^[^«$%&/()=*]{10,140}$/,
	edad: /^.{2}$/, // 4 a 12 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/, // 7 a 14 numeros.
	fecha : /^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/
}


var campos = {
	nombre: false,
	apellido: false,
	cedula: false,
	celular: false,
	edad: false,
	email: false,
	nacimiento: false,
	direccion: false,
	comentarios: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
        case "nombre":
                validarCampo(expresiones.nombre, e.target, 'nombre');
            break;
        case "apellido":
                validarCampo(expresiones.nombre, e.target, 'apellido');
            break;
        case "edad":
                validarCampo(expresiones.edad, e.target, 'edad');
            break;
        case "cedula":
                validarCampo(expresiones.numeros, e.target, 'cedula');
            break;
        case "email":
                validarCampo(expresiones.correo, e.target, 'email');
            break;
        case "celular":
                validarCampo(expresiones.numeros, e.target, 'celular');
            break;
        case "nacimiento":
                validarCampo(expresiones.fecha, e.target, 'nacimiento');
            break;
        case "direccion":
                validarCampo(expresiones.direccion, e.target, 'direccion');
            break;
        case "comentarios":
                validarCampo(expresiones.comentarios, e.target, 'comentarios');
            break;
    } 
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){

		input.classList.remove('incorrecto');
		input.classList.add('correcto');
		
		campos[campo] = true;
	} else {
		input.classList.add('incorrecto');
		input.classList.remove('correcto');
		
		campos[campo] = false;
	}
}

const cancelar_campos = document.getElementById('button-close-campos');
const modal = document.getElementById('contenedor-eliminar');
cancelar_campos.addEventListener("click", () => {
	modal.classList.remove("showeliminar")
});


inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});


textarea.addEventListener('keyup', validarFormulario);
textarea.addEventListener('blur', validarFormulario);


formulario.addEventListener('submit', (e) => {
	e.preventDefault();
	if (campos.nombre && campos.apellido&& campos.cedula && campos.celular && campos.email && campos.direccion  && campos.nacimiento  && campos.edad   && campos.comentarios){
		formulario.submit();
	}else{
		document.getElementById("sms").innerText = "Campos vacios o invalidos, por favor verificar antes de enviar";
		modal.classList.add("showeliminar");
	}
});