<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Dashboard.aspx.cs" Inherits="BibliotecaNormal.Dashboard" %>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Control - Biblioteca Digital</title>
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

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card-icon {
            font-size: 32px;
            color: #4c5af9;
            margin-bottom: 15px;
        }

        .card-value {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .card-label {
            font-size: 14px;
            color: #777;
            font-weight: 500;
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
    </style>
</head>
<body>
    <form id="form1" runat="server">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="logo">Biblioteca</div>
            <ul class="sidebar-menu">
                <li class="sidebar-menu-title">Dashboard</li>
                <li><a href="Dashboard.aspx" id="dashLink" runat="server"><span class="icon fas fa-chart-line"></span> Dashboard</a></li>
                <li class="sidebar-menu-title">Base de datos</li>
                <li><a href="Libros.aspx" id="librosLink" runat="server"><span class="icon fas fa-book"></span> Libros</a></li>
                <li><a href="Autores.aspx" id="autoresLink" runat="server"><span class="icon fas fa-user-edit"></span> Autores</a></li>
                <li><a href="Editoriales.aspx" id="editorialesLink" runat="server"><span class="icon fas fa-pen-nib"></span> Editoriales</a></li>
                <li><a href="Categorias.aspx" id="categoriasLink" runat="server"><span class="icon fas fa-tags"></span> Categorías</a></li>
                <li><a href="Idiomas.aspx" id="idiomasLink" runat="server"><span class="icon fas fa-language"></span> Idiomas</a></li>
                <li><a href="Lectores.aspx" id="lectoresLink" runat="server"><span class="icon fas fa-users"></span> Lectores</a></li>
                <li class="sidebar-menu-title">Préstamos</li>
                <li><a href="Prestamos.aspx" id="prestamosLink" runat="server"><span class="icon fas fa-handshake"></span> Préstamos</a></li>
                <li><a href="Devoluciones.aspx" id="devolucionesLink" runat="server"><span class="icon fas fa-undo-alt"></span> Devoluciones</a></li>
                <li class="sidebar-menu-title">Administración</li>
                <li><a href="Usuarios.aspx" id="usuariosLink" runat="server"><span class="icon fas fa-user-cog"></span> Usuarios</a></li>
                <li><a href="Reportes.aspx" id="reportesLink" runat="server"><span class="icon fas fa-chart-bar"></span> Reportes</a></li>
            </ul>
        </div>
    </form>
</body>
</html>
