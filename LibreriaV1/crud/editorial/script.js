const form = document.getElementById("editorialForm");
const tabla = document.getElementById("tablaEditoriales");

async function cargarEditoriales() {
  const res = await fetch("http://localhost:3000/api/editoriales");
  const editoriales = await res.json();
  renderEditoriales(editoriales);
}

function renderEditoriales(editoriales) {
  tabla.innerHTML = "";
  editoriales.forEach(e => {
    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td>${e.id}</td>
      <td>${e.nombre}</td>
      <td>${e.pais}</td>
      <td><button onclick="eliminarEditorial(${e.id})">Eliminar</button></td>
    `;
    tabla.appendChild(fila);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nombre = document.getElementById("nombre").value.trim();
  const pais = document.getElementById("pais").value.trim();

  if (!nombre) return alert("El nombre es obligatorio");

  await fetch("http://localhost:3000/api/editoriales", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre, pais })
  });

  form.reset();
  cargarEditoriales();
});

async function eliminarEditorial(id) {
  if (confirm("¿Eliminar editorial?")) {
    await fetch(`http://localhost:3000/api/editoriales/${id}`, { method: "DELETE" });
    cargarEditoriales();
  }
}

cargarEditoriales();
