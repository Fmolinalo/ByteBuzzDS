// ------------------ EDITORIALES ------------------
const formEditoriales = document.getElementById('editorialForm');
const tablaEditoriales = document.getElementById('tablaEditoriales');

// Cargar editoriales desde el servidor
async function cargarEditoriales() {
  try {
    const res = await fetch('http://localhost:3000/api/editoriales');
    const editoriales = await res.json();
    renderEditoriales(editoriales);
  } catch (err) {
    console.error('Error al cargar editoriales:', err);
  }
}

// Renderizar tabla de editoriales
function renderEditoriales(editoriales) {
  tablaEditoriales.innerHTML = '';
  editoriales.forEach(e => {
    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${e.EditorialID}</td>
      <td>${e.Nombre}</td>
      <td>${e.Telefono || '-'}</td>
      <td>${e.Email || '-'}</td>
      <td><button onclick="eliminarEditorial(${e.EditorialID})">Eliminar</button></td>
    `;
    tablaEditoriales.appendChild(fila);
  });
}

// Agregar nueva editorial
formEditoriales.addEventListener('submit', async e => {
  e.preventDefault();
  const Nombre = document.getElementById('nombreEd').value.trim();
  const Telefono = document.getElementById('telefono').value.trim();
  const Email = document.getElementById('email').value.trim();

  if (!Nombre) return alert('El nombre es obligatorio');

  try {
    await fetch('http://localhost:3000/api/editoriales', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ Nombre, Telefono, Email })
    });

    formEditoriales.reset();
    cargarEditoriales();
  } catch (err) {
    console.error('Error al agregar editorial:', err);
  }
});

// Eliminar editorial
async function eliminarEditorial(id) {
  if (confirm('¿Eliminar editorial?')) {
    try {
      await fetch(`http://localhost:3000/api/editoriales/${id}`, { method: 'DELETE' });
      cargarEditoriales();
    } catch (err) {
      console.error('Error al eliminar editorial:', err);
    }
  }
}

// Inicializar carga de editoriales al abrir la página
cargarEditoriales();
