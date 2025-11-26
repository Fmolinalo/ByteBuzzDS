import pyodbc
import random

def Actualizar():
    # Lista de servidores para conectar (Tu configuración robusta)
    servers = ['localhost', '.', r'.\SQLEXPRESS', r'localhost\SQLEXPRESS', r'MSI\SQLEXPRESS', 'MSI', '(local)']
    driver = '{ODBC Driver 17 for SQL Server}'
    conn = None

    print("🔍 Conectando a la base de datos...")
    for server in servers:
        try:
            conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE=pasteleria_db;Trusted_Connection=yes;', timeout=1)
            print(f"✅ Conectado a: {server}")
            break
        except: continue
    
    if not conn: return print("❌ No se pudo conectar.")

    cursor = conn.cursor()

    try:
        # --- 1. REPARAR EL ERROR DE CAJA (CRÍTICO) ---
        print("\n🛠️ Verificando Caja #1...")
        cursor.execute("SET IDENTITY_INSERT CAJA ON")
        
        cursor.execute("""
            IF NOT EXISTS (SELECT id_caja FROM CAJA WHERE id_caja = 1)
            BEGIN
                DECLARE @UserId INT = (SELECT TOP 1 id_usuario FROM USUARIO);
                INSERT INTO CAJA (id_caja, id_usuario, monto_inicial, estado, fecha_apertura)
                VALUES (1, @UserId, 100.00, 'abierta', GETDATE());
                PRINT '   -> Caja #1 creada exitosamente (Error solucionado)';
            END
            ELSE
            BEGIN
                PRINT '   -> La Caja #1 ya existe (Todo correcto)';
            END
        """)
        cursor.execute("SET IDENTITY_INSERT CAJA OFF")
        conn.commit()

        # --- 2. AGREGAR NUEVOS POSTRES ---
        print("\n🍰 Agregando nuevos postres al menú...")
        
        nuevos_productos = [
            (1, 'MIL-001', 'Milhojas de Manjar', 8.50, '🥧'),
            (1, 'PYE-001', 'Pye de Manzana', 12.00, '🍎'),
            (1, 'TRM-001', 'Tiramisú Clásico', 15.00, '☕'),
            (1, 'TRN-001', 'Turrón Doña Pepa', 18.00, '🍯'),
            (2, 'ALF-002', 'Alfajor de Maicena', 3.50, '🍪'),
            (2, 'CRE-001', 'Crema Volteada', 6.00, '🍮'),
            (2, 'LEC-001', 'Leche Asada', 5.50, '🥛'),
            (2, 'MUF-001', 'Muffin Arándanos', 4.50, '🧁'),
            (3, 'EMP-003', 'Empanada Mixta', 5.00, '🥟'),
            (1, 'SEL-001', 'Selva Negra', 55.00, '🍫')
        ]

        count = 0
        for cat, cod, nom, prec, img in nuevos_productos:
            # Verificar si el producto ya existe por código
            cursor.execute("SELECT id_producto FROM PRODUCTO WHERE codigo = ?", (cod,))
            if not cursor.fetchone():
                # Insertar Producto
                cursor.execute("""
                    INSERT INTO PRODUCTO (id_categoria, codigo, nombre, descripcion, precio_venta, stock_minimo, imagen_url, estado)
                    VALUES (?, ?, ?, 'Delicia artesanal fresca', ?, 5, ?, 1)
                """, (cat, cod, nom, prec, img))
                
                # Obtener el ID generado
                cursor.execute("SELECT @@IDENTITY")
                prod_id = cursor.fetchone()[0]
                
                # Insertar Inventario Inicial (Stock entre 20 y 50)
                stock = random.randint(20, 50)
                cursor.execute("INSERT INTO INVENTARIO (id_producto, stock_actual) VALUES (?, ?)", (prod_id, stock))
                
                print(f"   + Agregado: {nom}")
                count += 1
        
        conn.commit()
        
        if count > 0:
            print(f"\n✨ ¡Listo! Se agregaron {count} productos nuevos.")
        else:
            print("\n👍 Los productos ya estaban agregados.")

        print("\n✅ TODO LISTO. Reinicia tu página web para ver los cambios.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    Actualizar()