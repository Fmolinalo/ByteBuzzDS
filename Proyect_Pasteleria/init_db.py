import pyodbc
import time

def setup_database():
    server = 'localhost' # El servidor que sabemos que Python ve
    driver = '{ODBC Driver 17 for SQL Server}'
    
    print(f"🔌 Conectando a SQL Server en '{server}' para configuración inicial...")
    
    try:
        # 1. Conectar a 'master' para crear la base de datos
        conn_master = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE=master;Trusted_Connection=yes;', autocommit=True)
        cursor = conn_master.cursor()
        
        # Verificar si existe y crear
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'pasteleria_db'")
        if not cursor.fetchone():
            print("✨ Creando base de datos 'pasteleria_db'...")
            cursor.execute("CREATE DATABASE pasteleria_db")
        else:
            print("ℹ️ La base de datos 'pasteleria_db' ya existe.")
            
        conn_master.close()
        
        # 2. Conectar a la nueva base de datos para crear tablas
        print("📦 Configurando tablas y datos...")
        conn_db = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE=pasteleria_db;Trusted_Connection=yes;', autocommit=True)
        cursor = conn_db.cursor()
        
        # Script SQL completo
        sql_script = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CATEGORIA' AND xtype='U')
        BEGIN
            CREATE TABLE CATEGORIA (
                id_categoria INT IDENTITY(1,1) PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                descripcion VARCHAR(MAX),
                estado BIT DEFAULT 1
            );
        END

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='USUARIO' AND xtype='U')
        BEGIN
            CREATE TABLE USUARIO (
                id_usuario INT IDENTITY(1,1) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                rol VARCHAR(20) NOT NULL,
                telefono VARCHAR(15),
                estado BIT DEFAULT 1,
                fecha_creacion DATETIME DEFAULT GETDATE(),
                ultima_sesion DATETIME,
                CONSTRAINT CK_Usuario_Rol CHECK (rol IN ('admin', 'vendedor', 'cliente'))
            );
        END

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='PRODUCTO' AND xtype='U')
        BEGIN
            CREATE TABLE PRODUCTO (
                id_producto INT IDENTITY(1,1) PRIMARY KEY,
                id_categoria INT NOT NULL,
                codigo VARCHAR(20) UNIQUE,
                nombre VARCHAR(100) NOT NULL,
                descripcion VARCHAR(MAX),
                precio_venta DECIMAL(10,2) NOT NULL,
                precio_costo DECIMAL(10,2),
                unidad_medida VARCHAR(20) DEFAULT 'unidad',
                stock_minimo INT DEFAULT 5,
                imagen_url VARCHAR(255),
                estado BIT DEFAULT 1,
                fecha_creacion DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria)
            );
        END

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='INVENTARIO' AND xtype='U')
        BEGIN
            CREATE TABLE INVENTARIO (
                id_inventario INT IDENTITY(1,1) PRIMARY KEY,
                id_producto INT NOT NULL,
                stock_actual INT DEFAULT 0,
                stock_reservado INT DEFAULT 0,
                fecha_actualizacion DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
            );
        END
        
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CAJA' AND xtype='U')
        BEGIN
            CREATE TABLE CAJA (
                id_caja INT IDENTITY(1,1) PRIMARY KEY,
                id_usuario INT NOT NULL,
                monto_inicial DECIMAL(10,2) NOT NULL,
                monto_final DECIMAL(10,2),
                total_ventas DECIMAL(10,2) DEFAULT 0.00,
                total_efectivo DECIMAL(10,2) DEFAULT 0.00,
                total_digital DECIMAL(10,2) DEFAULT 0.00,
                diferencia DECIMAL(10,2) DEFAULT 0.00,
                estado VARCHAR(20) DEFAULT 'abierta',
                fecha_apertura DATETIME DEFAULT GETDATE(),
                fecha_cierre DATETIME,
                observaciones VARCHAR(MAX),
                FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
            );
        END

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='VENTA' AND xtype='U')
        BEGIN
            CREATE TABLE VENTA (
                id_venta INT IDENTITY(1,1) PRIMARY KEY,
                id_usuario INT NOT NULL,
                id_caja INT NOT NULL,
                numero_venta VARCHAR(20),
                fecha_venta DATETIME DEFAULT GETDATE(),
                subtotal DECIMAL(10,2) NOT NULL,
                descuento DECIMAL(10,2) DEFAULT 0.00,
                total DECIMAL(10,2) NOT NULL,
                metodo_pago VARCHAR(20) NOT NULL,
                estado VARCHAR(20) DEFAULT 'completada',
                cliente_nombre VARCHAR(100),
                observaciones VARCHAR(MAX),
                FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario),
                FOREIGN KEY (id_caja) REFERENCES CAJA(id_caja)
            );
        END

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='DETALLE_VENTA' AND xtype='U')
        BEGIN
            CREATE TABLE DETALLE_VENTA (
                id_detalle INT IDENTITY(1,1) PRIMARY KEY,
                id_venta INT NOT NULL,
                id_producto INT NOT NULL,
                cantidad INT NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                descuento_item DECIMAL(10,2) DEFAULT 0.00,
                FOREIGN KEY (id_venta) REFERENCES VENTA(id_venta),
                FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
            );
        END

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BOLETA' AND xtype='U')
        BEGIN
            CREATE TABLE BOLETA (
                id_boleta INT IDENTITY(1,1) PRIMARY KEY,
                id_venta INT NOT NULL UNIQUE,
                numero_boleta VARCHAR(20) NOT NULL,
                serie VARCHAR(10) NOT NULL,
                fecha_emision DATETIME DEFAULT GETDATE(),
                ruc_dni VARCHAR(11),
                nombre_cliente VARCHAR(100),
                direccion VARCHAR(255),
                formato VARCHAR(20) DEFAULT 'ticket',
                estado VARCHAR(20) DEFAULT 'emitida',
                FOREIGN KEY (id_venta) REFERENCES VENTA(id_venta)
            );
        END
        """
        
        # Ejecutar creación de tablas
        for statement in sql_script.split("END"):
            if statement.strip():
                cursor.execute(statement + "END")
        
        # Insertar datos iniciales si está vacía
        cursor.execute("SELECT COUNT(*) FROM CATEGORIA")
        if cursor.fetchone()[0] == 0:
            print("🌱 Insertando datos semilla...")
            cursor.execute("INSERT INTO CATEGORIA (nombre) VALUES ('General')")
            cursor.execute("INSERT INTO PRODUCTO (id_categoria, codigo, nombre, precio_venta, imagen_url) VALUES (1, 'P01', 'Torta Chocolate', 45.00, '🎂')")
            cursor.execute("INSERT INTO PRODUCTO (id_categoria, codigo, nombre, precio_venta, imagen_url) VALUES (1, 'P02', 'Cheesecake', 50.00, '🍰')")
            cursor.execute("INSERT INTO INVENTARIO (id_producto, stock_actual) VALUES (1, 100), (2, 100)")
            
        print("\n✅ ¡SISTEMA DE BASE DE DATOS REPARADO Y LISTO!")
        print("Ahora puedes ejecutar 'python app.py'")
        
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")

if __name__ == "__main__":
    setup_database()