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

