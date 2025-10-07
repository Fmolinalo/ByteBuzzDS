const select = document.getElementById('crudSelect');
const boton = document.getElementById('btnIr');

select.addEventListener('change', () => {
  boton.disabled = select.value === "";
});

boton.addEventListener('click', () => {
  const valor = select.value;
  if (valor === "editoriales") {
    window.location.href = "editorial/editorial-index.html";
  } else if (valor === "autores") {
    window.location.href = "autor/autor-index.html";
  } else if (valor === "categorias") {
    window.location.href = "categoria/categoria-index.html";
  }
});
