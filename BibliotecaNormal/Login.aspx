<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Login.aspx.cs" Inherits="BibliotecaNormal.Login" %>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Biblioteca Digital</title>
    <!-- Font Awesome para los iconos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Estilos en línea para un diseño moderno y centrado -->
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .login-card {
            background-color: #ffffff;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            padding: 40px;
            width: 100%;
            max-width: 400px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .login-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }

        .logo-container {
            margin-bottom: 20px;
        }

        .logo-icon {
            font-size: 48px;
            color: #4c5af9;
        }

        .app-title {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-top: 10px;
        }

        .subtitle {
            font-size: 14px;
            color: #777;
            margin-bottom: 30px;
        }

        .form-group {
            text-align: left;
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-size: 14px;
            font-weight: 500;
            color: #555;
            margin-bottom: 8px;
        }

        .input-group {
            position: relative;
        }

        .input-group input {
            width: 100%;
            padding: 12px 12px 12px 40px;
            border: 1px solid #ddd;
            border-radius: 10px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }

        .input-group input:focus {
            border-color: #4c5af9;
            box-shadow: 0 0 0 3px rgba(76, 90, 249, 0.2);
        }

        .input-group .icon {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #888;
        }

        .options-group {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .options-group a {
            color: #4c5af9;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .options-group a:hover {
            color: #3a47d3;
        }

        .checkbox-container {
            display: flex;
            align-items: center;
        }

        .checkbox-container input {
            margin-right: 8px;
        }

        .btn-login {
            width: 100%;
            padding: 15px;
            background-color: #4c5af9;
            color: #fff;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.1s ease;
        }

        .btn-login:hover {
            background-color: #3a47d3;
        }

        .btn-login:active {
            transform: scale(0.98);
        }
        
        .register-link {
            font-size: 14px;
            color: #555;
            margin-top: 30px;
        }

        .register-link a {
            color: #4c5af9;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .register-link a:hover {
            color: #3a47d3;
        }
        .error-message {
            color: red;
            font-size: 14px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <form id="form1" runat="server">
        <div class="login-card">
            <div class="logo-container">
                <i class="fas fa-book-reader logo-icon"></i>
            </div>
            <h1 class="app-title">Biblioteca Digital</h1>
            <p class="subtitle">Ingresa tus credenciales para acceder</p>

            <div class="form-group">
                <label for="txtUsername">Usuario</label>
                <div class="input-group">
                    <i class="fas fa-user icon"></i>
                    <asp:TextBox ID="txtUsername" runat="server" placeholder="Ingresa tu usuario"></asp:TextBox>
                </div>
            </div>

            <div class="form-group">
                <label for="txtPassword">Contraseña</label>
                <div class="input-group">
                    <i class="fas fa-lock icon"></i>
                    <asp:TextBox ID="txtPassword" runat="server" TextMode="Password" placeholder="Ingresa tu contraseña"></asp:TextBox>
                </div>
            </div>

            <div class="options-group">
                <div class="checkbox-container">
                    <asp:CheckBox ID="chkRememberMe" runat="server" Text="Recordarme" />
                </div>
                <a href="#">¿Olvidaste tu contraseña?</a>
            </div>

            <asp:Button ID="btnLogin" runat="server" Text="Ingresar" CssClass="btn-login" OnClick="btnLogin_Click" />
            
            <asp:Label ID="lblError" runat="server" ForeColor="Red" Visible="false" Text="Usuario o contraseña incorrectos." CssClass="error-message"></asp:Label>
            
            <p class="register-link">¿No tienes una cuenta? <a href="#">Regístrate aquí</a></p>
        </div>
    </form>
</body>
</html>
