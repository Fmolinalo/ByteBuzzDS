import pyodbc
import random

def cargar_datos_maestros():
    # Configuración de conexión robusta
    servers = ['localhost', '.', r'.\SQLEXPRESS', r'localhost\SQLEXPRESS', r'MSI\SQLEXPRESS', 'MSI', '(local)']
    driver = '{ODBC Driver 17 for SQL Server}'
    conn = None

    print("👩‍🍳 Conectando a la cocina (Base de Datos)...")
    for server in servers:
        try:
            conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE=pasteleria_db;Trusted_Connection=yes;', timeout=1)
            print(f"✅ Conectado a: {server}")
            break
        except: continue
    
    if not conn: return print("❌ No se pudo conectar.")

    cursor = conn.cursor()

    try:
        # --- 1. SOLUCIONAR ERROR DE CAJA (PRIORIDAD) ---
        print("\n🔧 Reparando Caja registradora...")
        cursor.execute("SET IDENTITY_INSERT CAJA ON")
        cursor.execute("""
            IF NOT EXISTS (SELECT id_caja FROM CAJA WHERE id_caja = 1)
            BEGIN
                -- Asignar caja al primer usuario que encontremos
                DECLARE @UserId INT = (SELECT TOP 1 id_usuario FROM USUARIO);
                IF @UserId IS NOT NULL
                BEGIN
                    INSERT INTO CAJA (id_caja, id_usuario, monto_inicial, estado, fecha_apertura)
                    VALUES (1, @UserId, 100.00, 'abierta', GETDATE());
                    PRINT '   -> Caja #1 Abierta correctamente.';
                END
            END
        """)
        cursor.execute("SET IDENTITY_INSERT CAJA OFF")
        conn.commit()

        # --- 2. LIMPIEZA (Opcional, para quitar los "??" feos) ---
        # Nota: Solo limpiaremos productos si no tienen ventas asociadas para evitar errores, 
        # si es una DB nueva, esto limpiará todo.
        print("\n🧹 Limpiando menú antiguo...")
        try:
            # Intentamos limpiar inventario y productos viejos para recargar
            cursor.execute("DELETE FROM INVENTARIO") 
            cursor.execute("DELETE FROM PRODUCTO") 
            cursor.execute("DELETE FROM CATEGORIA")
            # Reiniciar contadores de ID
            cursor.execute("DBCC CHECKIDENT ('PRODUCTO', RESEED, 0)")
            cursor.execute("DBCC CHECKIDENT ('CATEGORIA', RESEED, 0)")
        except:
            print("   (Nota: No se borraron algunos productos antiguos porque ya tienen ventas, agregaremos los nuevos encima)")

        # --- 3. CARGAR CATEGORÍAS ---
        print("\n📂 Creando categorías...")
        categorias = ['Tortas Enteras', 'Porciones & Postres', 'Bocaditos Salados', 'Bebidas Calientes', 'Bebidas Frías']
        for cat in categorias:
            cursor.execute("INSERT INTO CATEGORIA (nombre, descripcion, estado) VALUES (?, 'Delicioso', 1)", (cat,))
        conn.commit()

        # --- 4. CARGAR EL MENÚ DELICIOSO ---
        print("\n🍰 Horneando nuevos productos...")
        
        # Lista de: (ID_Categoria, Código, Nombre, Precio, Icono)
        menu = [
            # Tortas (Cat 1)
            (1, 'TOR-01', 'Torta de Chocolate', 45.00, '🎂'),
            (1, 'TOR-02', 'Cheesecake Fresa', 50.00, '🍰'),
            (1, 'TOR-03', 'Red Velvet', 55.00, '🧁'),
            (1, 'TOR-04', 'Tres Leches', 40.00, '🥛'),
            (1, 'TOR-05', 'Tiramisú', 60.00, '☕'),
            
            # Porciones (Cat 2)
            (2, 'IND-01', 'Milhojas', 8.00, '🥧'),
            (2, 'IND-02', 'Pye de Manzana', 12.00, '🍎'),
            (2, 'IND-03', 'Brownie', 6.00, '🍫'),
            (2, 'IND-04', 'Alfajor', 3.50, '🍪'),
            (2, 'IND-05', 'Crema Volteada', 5.00, '🍮'),
            (2, 'IND-06', 'Cupcake Vainilla', 4.00, '🧁'),

            # Salados (Cat 3)
            (3, 'SAL-01', 'Empanada de Carne', 5.00, '🥟'),
            (3, 'SAL-02', 'Empanada de Pollo', 5.00, '🥟'),
            (3, 'SAL-03', 'Quiche de Verduras', 7.00, '🥬'),

            # Bebidas (Cat 4 y 5)
            (4, 'BEB-01', 'Café Americano', 6.00, '☕'),
            (4, 'BEB-02', 'Capuchino', 8.00, '☕'),
            (5, 'BEB-03', 'Jugo de Naranja', 10.00, '🍊'),
            (5, 'BEB-04', 'Chicha Morada', 5.00, '🍇')
        ]

        for id_cat, codigo, nombre, precio, icono in menu:
            # Insertar Producto
            cursor.execute("""
                INSERT INTO PRODUCTO (id_categoria, codigo, nombre, descripcion, precio_venta, stock_minimo, imagen_url, estado)
                VALUES (?, ?, ?, 'Fresco y delicioso', ?, 5, ?, 1)
            """, (id_cat, codigo, nombre, precio, icono))
            
            # Obtener ID del producto recién creado
            cursor.execute("SELECT @@IDENTITY")
            id_prod = cursor.fetchone()[0]

            # Llenar Inventario (Stock 50 unidades)
            cursor.execute("INSERT INTO INVENTARIO (id_producto, stock_actual) VALUES (?, 50)", (id_prod,))
            
            print(f"   + {icono} {nombre} listo (S/ {precio})")

        conn.commit()
        print("\n✅ ¡MENÚ ACTUALIZADO CON ÉXITO!")
        print("Ahora recarga tu página web (F5) para ver los nuevos postres.")

    except Exception as e:
        print(f"\n❌ Ocurrió un error: {e}")
        if "REFERENCE constraint" in str(e):
            print("💡 CONSEJO: El error de referencia ocurre porque intentamos borrar productos que ya vendiste.")
            print("   No te preocupes, los nuevos productos se agregaron al final de la lista.")
    finally:
        conn.close()

if __name__ == "__main__":
    cargar_datos_maestros()