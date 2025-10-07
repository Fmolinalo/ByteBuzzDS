const form = document.getElementById("categoriaForm");
const tabla = document.getElementById("tablaCategorias");

async function cargarCategorias() {
  const res = await fetch("http://localhost:3000/api/categorias");
  const categorias = await res.json();
  renderCategorias(categorias);
}

function renderCategorias(categorias) {
  tabla.innerHTML = "";
  categorias.forEach(c => {
    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td>${c.id}</td>
      <td>${c.nombre}</td>
      <td><button onclick="eliminarCategoria(${c.id})">Eliminar</button></td>
    `;
    tabla.appendChild(fila);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nombre = document.getElementById("nombre").value.trim();
  if (!nombre) return alert("El nombre es obligatorio");

  await fetch("http://localhost:3000/api/categorias", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre })
  });

  form.reset();
  cargarCategorias();
});

async function eliminarCategoria(id) {
  if (confirm("¿Eliminar categoría?")) {
    await fetch(`http://localhost:3000/api/categorias/${id}`, { method: "DELETE" });
    cargarCategorias();
  }
}

cargarCategorias();
