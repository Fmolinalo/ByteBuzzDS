const form = document.getElementById('formAutores');
const tabla = document.querySelector('#tablaAutores tbody');
const btnCancelar = document.getElementById('btnCancelar');
const btnVolver = document.getElementById('btnVolver');

let editando = false;
let autorId = null;

// --- CARGAR AUTORES DESDE EL SERVIDOR ---
async function cargarAutores() {
  const res = await fetch('http://localhost:3000/api/autores');
  const autores = await res.json();
  renderTabla(autores);
}

// --- MOSTRAR TABLA ---
function renderTabla(autores) {
  tabla.innerHTML = '';

  autores.forEach(a => {
    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${a.id}</td>
      <td>${a.nombre}</td>
      <td>${a.nacionalidad || '-'}</td>
      <td>
        <button class="btn-accion btn-editar" onclick="editarAutor(${a.id}, '${a.nombre}', '${a.nacionalidad || ''}')">✏️</button>
        <button class="btn-accion btn-eliminar" onclick="eliminarAutor(${a.id})">🗑️</button>
      </td>
    `;
    tabla.appendChild(fila);
  });
}

// --- GUARDAR O ACTUALIZAR AUTOR ---
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const nombre = document.getElementById('nombre').value.trim();
  const nacionalidad = document.getElementById('nacionalidad').value.trim();

  if (!nombre) {
    alert('El nombre es obligatorio');
    return;
  }

  const data = { nombre, nacionalidad };

  if (editando) {
    await fetch(`http://localhost:3000/api/autores/${autorId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    editando = false;
    autorId = null;
  } else {
    await fetch('http://localhost:3000/api/autores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  form.reset();
  btnCancelar.classList.add('oculto');
  cargarAutores();
});

// --- EDITAR AUTOR ---
function editarAutor(id, nombre, nacionalidad) {
  autorId = id;
  document.getElementById('nombre').value = nombre;
  document.getElementById('nacionalidad').value = nacionalidad;

  editando = true;
  btnCancelar.classList.remove('oculto');
}

// --- ELIMINAR AUTOR ---
async function eliminarAutor(id) {
  if (confirm('¿Seguro que deseas eliminar este autor?')) {
    await fetch(`http://localhost:3000/api/autores/${id}`, { method: 'DELETE' });
    cargarAutores();
  }
}

// --- CANCELAR EDICIÓN ---
btnCancelar.addEventListener('click', () => {
  form.reset();
  editando = false;
  autorId = null;
  btnCancelar.classList.add('oculto');
});

// --- VOLVER ---
btnVolver.addEventListener('click', () => {
  window.location.href = "../index.html";
});

// 🔄 Al cargar la página
cargarAutores();
