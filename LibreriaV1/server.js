const express = require('express');
const cors = require('cors');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// 🔌 Conexión a la base de datos
const db = mysql.createConnection({
    host: 'apuqhawarina.com',
    port: 3306,
    user: 'apuqhawa_admin',
    password: 'Alex70396579',
    database: 'NOMBRE_DE_TU_BD' // 👈 aquí el nombre exacto de tu base de datos
});

db.connect(err => {
    if (err) throw err;
    console.log('✅ Conectado a la base de datos MySQL');
});

// ---------------------------------------------------------
// 🧱 CRUD AUTOR
// ---------------------------------------------------------
app.get('/api/autores', (req, res) => {
    db.query('SELECT * FROM autor', (err, rows) => {
        if (err) return res.status(500).json({ error: err });
        res.json(rows);
    });
});

app.post('/api/autores', (req, res) => {
    const { nombre, nacionalidad } = req.body;
    db.query('INSERT INTO autor (nombre, nacionalidad) VALUES (?, ?)', [nombre, nacionalidad], (err) => {
        if (err) return res.status(500).json({ error: err });
        res.json({ message: 'Autor agregado correctamente' });
    });
});

// 🔄 Actualizar autor
app.put('/api/autores/:id', (req, res) => {
  const { id } = req.params;
  const { nombre, nacionalidad } = req.body;
  db.query('UPDATE autor SET nombre = ?, nacionalidad = ? WHERE id = ?', [nombre, nacionalidad, id], (err) => {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: 'Autor actualizado correctamente' });
  });
});

// 🗑️ Eliminar autor
app.delete('/api/autores/:id', (req, res) => {
  const { id } = req.params;
  db.query('DELETE FROM autor WHERE id = ?', [id], (err) => {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: 'Autor eliminado correctamente' });
  });
});


// ---------------------------------------------------------
// 🧱 CRUD CATEGORIA
// ---------------------------------------------------------
app.get('/api/categorias', (req, res) => {
    db.query('SELECT * FROM categoria', (err, rows) => {
        if (err) return res.status(500).json({ error: err });
        res.json(rows);
    });
});

app.post('/api/categorias', (req, res) => {
    const { nombre } = req.body;
    db.query('INSERT INTO categoria (nombre) VALUES (?)', [nombre], (err) => {
        if (err) return res.status(500).json({ error: err });
        res.json({ message: 'Categoría agregada correctamente' });
    });
});

// 🔄 Eliminar categoría
app.delete('/api/categorias/:id', (req, res) => {
  const { id } = req.params;
  db.query('DELETE FROM categoria WHERE id = ?', [id], (err) => {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: 'Categoría eliminada correctamente' });
  });
});

// ---------------------------------------------------------
// 🧱 CRUD EDITORIAL
// ---------------------------------------------------------
app.get('/api/editoriales', (req, res) => {
    db.query('SELECT * FROM editorial', (err, rows) => {
        if (err) return res.status(500).json({ error: err });
        res.json(rows);
    });
});

app.post('/api/editoriales', (req, res) => {
    const { nombre, pais } = req.body;
    db.query('INSERT INTO editorial (nombre, pais) VALUES (?, ?)', [nombre, pais], (err) => {
        if (err) return res.status(500).json({ error: err });
        res.json({ message: 'Editorial agregada correctamente' });
    });
});

// 🗑️ Eliminar editorial
app.delete('/api/editoriales/:id', (req, res) => {
  const { id } = req.params;
  db.query('DELETE FROM editorial WHERE id = ?', [id], (err) => {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: 'Editorial eliminada correctamente' });
  });
});

// ---------------------------------------------------------

const PORT = 3000;
app.listen(PORT, () => console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`));
