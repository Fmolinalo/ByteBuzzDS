import pyodbc

def fix_caja():
    # Lista de servidores para probar conexión (igual que en tu app)
    servers = ['localhost', '.', r'.\SQLEXPRESS', r'localhost\SQLEXPRESS', r'MSI\SQLEXPRESS', 'MSI', '(local)']
    driver = '{ODBC Driver 17 for SQL Server}'
    conn = None

    print("🔍 Buscando base de datos...")
    for server in servers:
        try:
            conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE=pasteleria_db;Trusted_Connection=yes;', timeout=1)
            print(f"✅ Conectado a: {server}")
            break
        except: continue
    
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor()
    
    try:
        # 1. Verificar si ya existe la Caja 1
        print("📦 Verificando Cajas...")
        cursor.execute("SELECT id_caja FROM CAJA WHERE id_caja = 1")
        if cursor.fetchone():
            print("✅ La Caja #1 ya existe. No se necesitan cambios.")
        else:
            # 2. Buscar un usuario para asignarle la caja (Necesitamos un responsable)
            print("⚠️ No hay caja abierta. Buscando un usuario responsable...")
            cursor.execute("SELECT TOP 1 id_usuario FROM USUARIO")
            user = cursor.fetchone()
            
            if not user:
                print("❌ ERROR: No hay usuarios registrados. Por favor regístrate en la web primero.")
                return
            
            user_id = user[0]
            
            # 3. Insertar la Caja #1
            print(f"🛠️ Abriendo Caja #1 asignada al usuario ID {user_id}...")
            cursor.execute("""
                SET IDENTITY_INSERT CAJA ON;
                INSERT INTO CAJA (id_caja, id_usuario, monto_inicial, estado, fecha_apertura)
                VALUES (1, ?, 100.00, 'abierta', GETDATE());
                SET IDENTITY_INSERT CAJA OFF;
            """, (user_id,))
            conn.commit()
            print("✅ ¡ÉXITO! Caja #1 creada correctamente.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_caja()