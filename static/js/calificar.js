const formulario = document.getElementById('form_coment');
const inputs = document.querySelectorAll('#form_coment input');
const textarea = document.querySelectorAll('#form_coment textarea');

const expresiones = {
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,350}$/,
	fecha : /^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/
}


const cancelar = document.getElementById('button-close-campos');
const modal = document.getElementById('contenedor-eliminar');
cancelar.addEventListener("click", () => {
	modal.classList.remove("showeliminar")
});


const campos = {
    comentario: false,
    fecha: false,
}

const validarFormulario = (e) => {
    console.log(e.target.name);
	switch (e.target.name) {
    case "comentario":
			validarCampo(expresiones.nombre, e.target, 'comentario');
		break;
    case "fcalificacion":
			validarCampo(expresiones.fecha, e.target, 'fecha');
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

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

textarea.forEach((textarea) => {
	textarea.addEventListener('keyup', validarFormulario);
	textarea.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	e.preventDefault();
	if (campos.comentario && campos.fecha){
		formulario.submit();
	}else{
		document.getElementById("sms").innerText = "Campos vacios o invalidos, por favor verificar antes de enviar";
		modal.classList.add("showeliminar");
	}
});