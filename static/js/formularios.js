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