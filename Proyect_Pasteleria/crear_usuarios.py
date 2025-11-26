import pyodbc

def crear_usuarios_base():
    # Configuración de conexión (Igual que tu app)
    server = 'localhost'
    driver = '{ODBC Driver 17 for SQL Server}'
    database = 'pasteleria_db'
    
    print(f"🔌 Conectando a {server} para crear usuarios...")
    
    try:
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        # Lista de usuarios a crear (Admin y Vendedores)
        usuarios = [
            ('Madre Superiora', 'admin@santateresa.com', 'password_seguro', 'admin', '987654321'),
            ('Flor Camila', 'flor@bytebuzz.com', 'vendedor123', 'vendedor', '999888777'),
            ('Ruth Sara', 'ruth@bytebuzz.com', 'vendedor123', 'vendedor', '999888666')
        ]

        count = 0
        for nombre, email, password, rol, telefono in usuarios:
            # Verificar si ya existe
            cursor.execute("SELECT id_usuario FROM USUARIO WHERE email = ?", (email,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO USUARIO (nombre, email, password, rol, telefono, estado)
                    VALUES (?, ?, ?, ?, ?, 1)
                """, (nombre, email, password, rol, telefono))
                print(f"✅ Usuario creado: {nombre} ({rol})")
                count += 1
            else:
                print(f"ℹ️ El usuario {email} ya existe.")
        
        conn.commit()
        
        if count > 0:
            print("\n🎉 ¡Usuarios creados exitosamente!")
        else:
            print("\n👍 Todos los usuarios ya existían.")
            
        print("\n🔐 CREDENCIALES DE ACCESO:")
        print("   Admin:    admin@santateresa.com / password_seguro")
        print("   Vendedor: flor@bytebuzz.com     / vendedor123")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    crear_usuarios_base()