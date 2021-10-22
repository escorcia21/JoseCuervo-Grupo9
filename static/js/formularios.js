const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const selects = document.querySelectorAll('#formulario select');

const expresiones = {
	//usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
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
	ingreso: false,
	termino: false,
	salario: false,
	tipo: false,
	direccion: false,
	estado: false
}

let r = window.location.href.split("/")[3];
if (r == "actualizar"){
	campos = {
		nombre: true,
		apellido: true,
		cedula: true,
		celular: true,
		edad: true,
		email: true,
		nacimiento: true,
		ingreso: true,
		termino: true,
		salario: true,
		tipo: true,
		direccion: true,
		estado: true
	}
}



// formularios
const input = document.getElementById("upload");
const txt = document.getElementById("txt");

input.addEventListener("change", ()=> {
  const path = input.value.split('\\');
  const file = path[path.length - 1];
  txt.innerText = file ? file : "Sube una foto";
});

let user = window.location.href.split("/");
if (user[4] != undefined || user[3] == "solicitud"){
  var a = document.getElementById("cc").disabled = true;
}

// comprovacion formularios

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
    case "tipo":
			validarCampo(expresiones.nombre, e.target, 'tipo');
		break;
    case "salario":
			validarCampo(expresiones.numeros, e.target, 'salario');
		break;
    case "ingreso":
			validarCampo(expresiones.fecha, e.target, 'ingreso');
		break;
    case "nacimiento":
			validarCampo(expresiones.fecha, e.target, 'nacimiento');
		break;
    case "termino":
			validarCampo(expresiones.fecha, e.target, 'termino');
		break;
    case "direccion":
			validarCampo(expresiones.direccion, e.target, 'direccion');
		break;
    case "estado_civil":
			validarCampo(expresiones.nombre, e.target, 'estado');
		break;
	
    
  }  
  //console.log(e.target.name);
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

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	e.preventDefault();
	if (campos.nombre && campos.apellido&& campos.cedula && campos.celular && campos.email && campos.direccion && campos.tipo && campos.ingreso && campos.nacimiento && campos.termino && campos.salario && campos.edad && campos.estado){
		formulario.submit();
	}
});