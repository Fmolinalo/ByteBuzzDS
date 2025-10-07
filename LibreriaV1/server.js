// server.js
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sql = require('mssql');

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// 🔌 Configuración de conexión SQL Server (Somee)
const config = {
  user: 'Cam_SQLLogin_1',
  password: 'kfr1tawwcz', // tu contraseña
  database: 'BibliotecaDS', // nombre exacto de tu BD
  server: 'BibliotecaDS.mssql.somee.com',
  options: {
    encrypt: true,
    trustServerCertificate: true
  }
};

// Conexión a SQL Server y arranque del servidor
sql.connect(config)
  .then(() => {
    console.log('✅ Conectado a SQL Server en Somee');
    
    const PORT = 3000;
    app.listen(PORT, () => {
      console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
    });

  })
  .catch(err => console.error('❌ Error de conexión:', err));

// ---------------------------------------------------------
// 🧱 CRUD AUTORES
// ---------------------------------------------------------
app.get('/api/autores', async (req, res) => {
  try {
    const result = await sql.query('SELECT AutorID, Nombre, Apellido, Nacionalidad, FechaNacimiento FROM Autores');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/autores', async (req, res) => {
  const { Nombre, Apellido, Nacionalidad, FechaNacimiento } = req.body;
  try {
    await sql.query`INSERT INTO Autores (Nombre, Apellido, Nacionalidad, FechaNacimiento) 
                    VALUES (${Nombre}, ${Apellido}, ${Nacionalidad}, ${FechaNacimiento})`;
    res.json({ message: 'Autor agregado correctamente' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.put('/api/autores/:id', async (req, res) => {
  const { id } = req.params;
  const { Nombre, Apellido, Nacionalidad, FechaNacimiento } = req.body;
  try {
    await sql.query`UPDATE Autores 
                    SET Nombre=${Nombre}, Apellido=${Apellido}, Nacionalidad=${Nacionalidad}, FechaNacimiento=${FechaNacimiento} 
                    WHERE AutorID=${id}`;
    res.json({ message: 'Autor actualizado correctamente' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/autores/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await sql.query`DELETE FROM Autores WHERE AutorID=${id}`;
    res.json({ message: 'Autor eliminado correctamente' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ---------------------------------------------------------
// 🧱 CRUD CATEGORIAS
// ---------------------------------------------------------
app.get('/api/categorias', async (req, res) => {
  try {
    const result = await sql.query('SELECT CategoriaID, Nombre, Descripcion FROM Categorias');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/categorias', async (req, res) => {
  const { Nombre, Descripcion } = req.body; // Deben venir con mayúscula inicial
  try {
    await sql.query`INSERT INTO Categorias (Nombre, Descripcion) VALUES (${Nombre}, ${Descripcion})`;
    res.json({ message: 'Categoría agregada correctamente' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/categorias/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await sql.query`DELETE FROM Categorias WHERE CategoriaID=${id}`;
    res.json({ message: 'Categoría eliminada correctamente' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ---------------------------------------------------------
// 🧱 CRUD EDITORIALES
// ---------------------------------------------------------

// Obtener todas las editoriales
app.get('/api/editoriales', async (req, res) => {
  try {
    const result = await sql.query('SELECT EditorialID, Nombre, Telefono, Email FROM Editoriales');
    res.json(result.recordset); // recordset es un array
  } catch (err) {
    console.error('Error en GET /api/editoriales:', err);
    res.status(500).json({ error: err.message });
  }
});

// Agregar nueva editorial
app.post('/api/editoriales', async (req, res) => {
  const { Nombre, Telefono, Email } = req.body;
  try {
    await sql.query`INSERT INTO Editoriales (Nombre, Telefono, Email) VALUES (${Nombre}, ${Telefono}, ${Email})`;
    res.json({ message: 'Editorial agregada correctamente' });
  } catch (err) {
    console.error('Error en POST /api/editoriales:', err);
    res.status(500).json({ error: err.message });
  }
});

// Eliminar editorial
app.delete('/api/editoriales/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await sql.query`DELETE FROM Editoriales WHERE EditorialID=${id}`;
    res.json({ message: 'Editorial eliminada correctamente' });
  } catch (err) {
    console.error('Error en DELETE /api/editoriales/:id:', err);
    res.status(500).json({ error: err.message });
  }
});
