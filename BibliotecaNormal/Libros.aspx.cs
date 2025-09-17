using System;
using System.Linq;
using System.Web.UI;
using BibliotecaNormal.Models;
using System.Data.Entity;

namespace BibliotecaNormal
{
    public partial class Libros : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                CargarLibros();
            }
        }

        // Cargar los datos de Libros en el GridView y los DropDownLists
        private void CargarLibros()
        {
            using (var db = new BibliotecaDBEntities1())
            {
                // Cargar datos para la tabla
                var libros = db.Libro.Include("Categoria").Include("Idioma").ToList();
                gvLibros.DataSource = libros;
                gvLibros.DataBind();

                // Cargar datos para los DropDownLists y ListBoxes
                var categorias = db.Categoria.ToList();
                ddlCategorias.DataSource = categorias;
                ddlCategorias.DataTextField = "nombre";
                ddlCategorias.DataValueField = "id_categoria";
                ddlCategorias.DataBind();

                var idiomas = db.Idioma.ToList();
                ddlIdiomas.DataSource = idiomas;
                ddlIdiomas.DataTextField = "nombre";
                ddlIdiomas.DataValueField = "id_idioma";
                ddlIdiomas.DataBind();

                var autores = db.Autor.ToList();
                lbAutores.DataSource = autores;
                lbAutores.DataTextField = "nombre";
                lbAutores.DataValueField = "id_autor";
                lbAutores.DataBind();

                var editoriales = db.Editorial.ToList();
                lbEditoriales.DataSource = editoriales;
                lbEditoriales.DataTextField = "nombre";
                lbEditoriales.DataValueField = "id_editorial";
                lbEditoriales.DataBind();
            }
        }

        // Manejar el evento del botón Guardar/Actualizar libro
        protected void btnGuardarLibro_Click(object sender, EventArgs e)
        {
            using (var db = new BibliotecaDBEntities1())
            {
                int libroId = string.IsNullOrEmpty(hfLibroId.Value) ? 0 : int.Parse(hfLibroId.Value);
                Libro libro;
                if (libroId == 0)
                {
                    // Crear nuevo libro
                    libro = new Libro();
                    db.Libro.Add(libro);
                }
                else
                {
                    // Actualizar libro existente
                    libro = db.Libro.Find(libroId);
                }

                libro.titulo = txtTitulo.Text;
                libro.isbn = txtISBN.Text;
                libro.anio_publicacion = int.Parse(txtAnioPublicacion.Text);
                libro.num_paginas = int.Parse(txtNumPaginas.Text);
                libro.ejemplares_disponibles = int.Parse(txtEjemplares.Text);
                libro.id_categoria = int.Parse(ddlCategorias.SelectedValue);
                libro.id_idioma = int.Parse(ddlIdiomas.SelectedValue);

                // Manejar las relaciones muchos a muchos
                libro.Autor.Clear();
                foreach (var item in lbAutores.Items.Cast<System.Web.UI.WebControls.ListItem>().Where(li => li.Selected))
                {
                    var autor = db.Autor.Find(int.Parse(item.Value));
                    if (autor != null)
                    {
                        libro.Autor.Add(autor);
                    }
                }

                libro.Editorial.Clear();
                foreach (var item in lbEditoriales.Items.Cast<System.Web.UI.WebControls.ListItem>().Where(li => li.Selected))
                {
                    var editorial = db.Editorial.Find(int.Parse(item.Value));
                    if (editorial != null)
                    {
                        libro.Editorial.Add(editorial);
                    }
                }

                db.SaveChanges();
            }

            // Limpiar formulario y recargar datos
            LimpiarFormulario();
            CargarLibros();
        }

        // Manejar el evento de edición de fila
        protected void gvLibros_RowEditing(object sender, System.Web.UI.WebControls.GridViewEditEventArgs e)
        {
            gvLibros.EditIndex = e.NewEditIndex;
            int libroId = Convert.ToInt32(gvLibros.DataKeys[e.NewEditIndex].Value);

            using (var db = new BibliotecaDBEntities1())
            {
                var libro = db.Libro.Include("Autor").Include("Editorial").FirstOrDefault(l => l.id_libro == libroId);
                if (libro != null)
                {
                    hfLibroId.Value = libro.id_libro.ToString();
                    txtTitulo.Text = libro.titulo;
                    txtISBN.Text = libro.isbn;
                    txtAnioPublicacion.Text = libro.anio_publicacion.ToString();
                    txtNumPaginas.Text = libro.num_paginas.ToString();
                    txtEjemplares.Text = libro.ejemplares_disponibles.ToString();
                    ddlCategorias.SelectedValue = libro.id_categoria.ToString();
                    ddlIdiomas.SelectedValue = libro.id_idioma.ToString();

                    // Seleccionar autores
                    foreach (System.Web.UI.WebControls.ListItem item in lbAutores.Items)
                    {
                        item.Selected = libro.Autor.Any(a => a.id_autor.ToString() == item.Value);
                    }

                    // Seleccionar editoriales
                    foreach (System.Web.UI.WebControls.ListItem item in lbEditoriales.Items)
                    {
                        item.Selected = libro.Editorial.Any(ed => ed.id_editorial.ToString() == item.Value);
                    }
                }
            }

            btnGuardarLibro.Text = "Actualizar";
            btnCancelar.Visible = true;
            CargarLibros();
        }

        // Manejar el evento de eliminación de fila
        protected void gvLibros_RowDeleting(object sender, System.Web.UI.WebControls.GridViewDeleteEventArgs e)
        {
            int libroId = Convert.ToInt32(gvLibros.DataKeys[e.RowIndex].Value);
            using (var db = new BibliotecaDBEntities1())
            {
                var libro = db.Libro.Find(libroId);
                if (libro != null)
                {
                    // Eliminar relaciones muchos a muchos antes de eliminar el libro
                    libro.Autor.Clear();
                    libro.Editorial.Clear();
                    db.SaveChanges();

                    db.Libro.Remove(libro);
                    db.SaveChanges();
                }
            }
            CargarLibros();
        }

        // Limpiar el formulario
        protected void btnCancelar_Click(object sender, EventArgs e)
        {
            LimpiarFormulario();
        }

        private void LimpiarFormulario()
        {
            hfLibroId.Value = string.Empty;
            txtTitulo.Text = string.Empty;
            txtISBN.Text = string.Empty;
            txtAnioPublicacion.Text = string.Empty;
            txtNumPaginas.Text = string.Empty;
            txtEjemplares.Text = string.Empty;
            ddlCategorias.SelectedIndex = -1;
            ddlIdiomas.SelectedIndex = -1;
            lbAutores.ClearSelection();
            lbEditoriales.ClearSelection();
            btnGuardarLibro.Text = "Guardar";
            btnCancelar.Visible = false;
        }
    }
}
