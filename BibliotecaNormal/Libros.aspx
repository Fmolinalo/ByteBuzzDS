<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Libros.aspx.cs" Inherits="BibliotecaNormal.Libros" %>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Libros - Biblioteca Digital</title>
    <!-- Font Awesome para los iconos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Fonts para Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f4f9;
            margin: 0;
            display: flex;
            color: #333;
        }

        /* Sidebar styles */
        .sidebar {
            width: 250px;
            background-color: #4c5af9;
            color: white;
            padding: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
        }

        .sidebar .logo {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 30px;
            text-align: center;
        }

        .sidebar-menu {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .sidebar-menu-title {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.6);
            margin: 20px 0 10px;
            text-transform: uppercase;
            font-weight: 600;
        }

        .sidebar-menu li a {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            margin-bottom: 5px;
            transition: background-color 0.3s ease;
        }

        .sidebar-menu li a.active,
        .sidebar-menu li a:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        .sidebar-menu li a .icon {
            margin-right: 15px;
            font-size: 18px;
            width: 20px;
            text-align: center;
        }

        /* Main Content styles */
        .main-content {
            flex-grow: 1;
            padding: 30px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 24px;
            font-weight: 700;
            margin: 0;
        }

        .table-section {
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            padding: 30px;
            margin-bottom: 30px;
        }

        .table-section h2 {
            font-size: 20px;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 20px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
        }

        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
            font-size: 14px;
        }

        .data-table th {
            font-weight: 600;
            color: #555;
            background-color: #fafafa;
        }

        .data-table tr:hover {
            background-color: #f9f9f9;
        }
        
        /* Form styles */
        .form-section {
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .form-group input[type="text"],
        .form-group input[type="number"],
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 14px;
        }
        
        .btn-primary, .btn-secondary {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .btn-primary {
            background-color: #4c5af9;
            color: white;
        }
        
        .btn-secondary {
            background-color: #e0e0e0;
            color: #333;
        }
        
        .btn-primary:hover {
            background-color: #3b45e6;
        }
        
        .btn-secondary:hover {
            background-color: #d0d0d0;
        }
        
        .action-links a {
            margin-right: 10px;
            color: #4c5af9;
            text-decoration: none;
        }
        
        .action-links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <form id="form1" runat="server">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="logo">Biblioteca</div>
            <ul class="sidebar-menu">
                <li class="sidebar-menu-title">Dashboard</li>
                <li><a href="Dashboard.aspx"><span class="icon fas fa-chart-line"></span> Dashboard</a></li>
                <li class="sidebar-menu-title">Base de datos</li>
                <li><a href="Libros.aspx" class="active"><span class="icon fas fa-book"></span> Libros</a></li>
                <li><a href="Autores.aspx"><span class="icon fas fa-user-edit"></span> Autores</a></li>
                <li><a href="Editoriales.aspx"><span class="icon fas fa-pen-nib"></span> Editoriales</a></li>
                <li><a href="Categorias.aspx"><span class="icon fas fa-tags"></span> Categorías</a></li>
                <li><a href="Idiomas.aspx"><span class="icon fas fa-language"></span> Idiomas</a></li>
                <li><a href="Lectores.aspx"><span class="icon fas fa-users"></span> Lectores</a></li>
                <li class="sidebar-menu-title">Préstamos</li>
                <li><a href="Prestamos.aspx"><span class="icon fas fa-handshake"></span> Préstamos</a></li>
                <li><a href="Devoluciones.aspx"><span class="icon fas fa-undo-alt"></span> Devoluciones</a></li>
                <li class="sidebar-menu-title">Administración</li>
                <li><a href="Usuarios.aspx"><span class="icon fas fa-user-cog"></span> Usuarios</a></li>
                <li><a href="Reportes.aspx"><span class="icon fas fa-chart-bar"></span> Reportes</a></li>
            </ul>
        </div>

        <!-- Main Content (Books Management Panel) -->
        <div class="main-content">
            <div class="header">
                <h1>Gestión de Libros</h1>
            </div>
            <div class="form-section">
                <asp:HiddenField ID="hfLibroId" runat="server" />
                <div class="form-group">
                    <label for="txtTitulo">Título</label>
                    <asp:TextBox ID="txtTitulo" runat="server"></asp:TextBox>
                </div>
                <div class="form-group">
                    <label for="txtISBN">ISBN</label>
                    <asp:TextBox ID="txtISBN" runat="server"></asp:TextBox>
                </div>
                <div class="form-group">
                    <label for="txtAnioPublicacion">Año de Publicación</label>
                    <asp:TextBox ID="txtAnioPublicacion" runat="server" TextMode="Number"></asp:TextBox>
                </div>
                <div class="form-group">
                    <label for="txtNumPaginas">Número de Páginas</label>
                    <asp:TextBox ID="txtNumPaginas" runat="server" TextMode="Number"></asp:TextBox>
                </div>
                <div class="form-group">
                    <label for="txtEjemplares">Ejemplares Disponibles</label>
                    <asp:TextBox ID="txtEjemplares" runat="server" TextMode="Number"></asp:TextBox>
                </div>
                <div class="form-group">
                    <label for="ddlCategorias">Categoría</label>
                    <asp:DropDownList ID="ddlCategorias" runat="server"></asp:DropDownList>
                </div>
                <div class="form-group">
                    <label for="ddlIdiomas">Idioma</label>
                    <asp:DropDownList ID="ddlIdiomas" runat="server"></asp:DropDownList>
                </div>
                <div class="form-group">
                    <label for="lbAutores">Autores</label>
                    <asp:ListBox ID="lbAutores" runat="server" SelectionMode="Multiple"></asp:ListBox>
                </div>
                <div class="form-group">
                    <label for="lbEditoriales">Editoriales</label>
                    <asp:ListBox ID="lbEditoriales" runat="server" SelectionMode="Multiple"></asp:ListBox>
                </div>
                <div class="form-group">
                    <asp:Button ID="btnGuardarLibro" runat="server" Text="Guardar" CssClass="btn-primary" OnClick="btnGuardarLibro_Click" />
                    <asp:Button ID="btnCancelar" runat="server" Text="Cancelar" CssClass="btn-secondary" OnClick="btnCancelar_Click" Visible="false" />
                </div>
            </div>

            <div class="table-section">
                <h2>Listado de Libros</h2>
                <asp:GridView ID="gvLibros" runat="server" AutoGenerateColumns="false" CssClass="data-table" DataKeyNames="id_libro" OnRowEditing="gvLibros_RowEditing" OnRowDeleting="gvLibros_RowDeleting">
                    <Columns>
                        <asp:BoundField DataField="titulo" HeaderText="Título" />
                        <asp:BoundField DataField="anio_publicacion" HeaderText="Año" />
                        <asp:BoundField DataField="num_paginas" HeaderText="Páginas" />
                        <asp:BoundField DataField="ejemplares_disponibles" HeaderText="Ejemplares" />
                        <asp:TemplateField HeaderText="Categoría">
                            <ItemTemplate>
                                <asp:Label runat="server" Text='<%# Eval("Categoria.nombre") %>'></asp:Label>
                            </ItemTemplate>
                        </asp:TemplateField>
                        <asp:TemplateField HeaderText="Idioma">
                            <ItemTemplate>
                                <asp:Label runat="server" Text='<%# Eval("Idioma.nombre") %>'></asp:Label>
                            </ItemTemplate>
                        </asp:TemplateField>
                        <asp:TemplateField HeaderText="Acciones">
                            <ItemTemplate>
                                <div class="action-links">
                                    <asp:LinkButton runat="server" CommandName="Edit" CommandArgument='<%# Eval("id_libro") %>'>Editar</asp:LinkButton>
                                    <asp:LinkButton runat="server" CommandName="Delete" CommandArgument='<%# Eval("id_libro") %>' OnClientClick="return confirm('¿Estás seguro de que quieres eliminar este libro?');">Eliminar</asp:LinkButton>
                                </div>
                            </ItemTemplate>
                        </asp:TemplateField>
                    </Columns>
                </asp:GridView>
            </div>
        </div>
    </form>
</body>
</html>
