const activo = document.getElementById('contenedor-nuevo');
const cancelar = document.getElementById('button-close-disponible');
const input_delete =document.getElementsByName('disponibilidad__cedula')[0];
const formulario_delete = document.getElementById('form_disponible');

function buscar() {
  var input, filter, table, li, i, txtValue;
  input = document.getElementById("search-box");
  filter = input.value;

  table = document.getElementById("tabla");
  li = table.getElementsByTagName("li");
  
  for (i = 0; i < li.length; i++) {
    r = li[i].getElementsByTagName("p")[1];
    if (r) {
      txtValue = r.textContent || r.innerText;
      if (txtValue.indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }       
  }
}

// dashboard
let url = window.location.href.split("/")[4];
if (url != undefined){
  //console.log(url)
  let editar = document.getElementById("editar");
  let calificar = document.getElementById("calificar");

  editar.href = `/actualizar/${url}`
  calificar.href = `/calificar/${url}`
}


function disponible(cc) {
  activo.classList.add('showeditar');
  document.getElementById("txt_disponible").innerHTML = `Confirme la cedula ${cc} para eliminar al usuario`;
  input_delete.placeholder  = cc;
}

cancelar.addEventListener("click", () => {
	activo.classList.remove("showeditar");
});

formulario_delete.addEventListener("submit",(e)=>{
  let a = input_delete.value;
  e.preventDefault();
  if (a == input_delete.placeholder){
    formulario_delete.submit();
  }
});