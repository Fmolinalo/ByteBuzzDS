const form = document.getElementById("categoriaForm");
const tabla = document.getElementById("tablaCategorias");

async function cargarCategorias() {
  try {
    const res = await fetch("http://localhost:3000/api/categorias");
    const categorias = await res.json();
    renderCategorias(categorias);
  } catch (err) {
    console.error("Error al cargar categorías:", err);
  }
}

function renderCategorias(categorias) {
  tabla.innerHTML = "";
  categorias.forEach(c => {
    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td>${c.CategoriaID}</td>
      <td>${c.Nombre}</td>
      <td>${c.Descripcion || '-'}</td>
      <td>
        <button onclick="eliminarCategoria(${c.CategoriaID})">Eliminar</button>
      </td>
    `;
    tabla.appendChild(fila);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nombre = document.getElementById("nombre").value.trim();
  const descripcion = document.getElementById("descripcion").value.trim();

  if (!nombre) return alert("El nombre es obligatorio");

  try {
    await fetch("http://localhost:3000/api/categorias", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ Nombre: nombre, Descripcion: descripcion })
    });
    form.reset();
    cargarCategorias();
  } catch (err) {
    console.error("Error al agregar categoría:", err);
  }
});

async function eliminarCategoria(id) {
  if (confirm("¿Eliminar categoría?")) {
    try {
      await fetch(`http://localhost:3000/api/categorias/${id}`, { method: "DELETE" });
      cargarCategorias();
    } catch (err) {
      console.error("Error al eliminar categoría:", err);
    }
  }
}

cargarCategorias();
