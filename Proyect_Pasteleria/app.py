import pyodbc
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CONFIGURACIÓN CORS MÁS PERMISIVA PARA EVITAR BLOQUEOS
CORS(app, resources={r"/*": {"origins": "*"}})

# --- CONEXIÓN INTELIGENTE ---
def get_db_connection():
    servers = [
        'localhost', '.', r'.\SQLEXPRESS', r'localhost\SQLEXPRESS', 
        r'MSI\SQLEXPRESS', 'MSI', '(local)'
    ]
    driver = '{ODBC Driver 17 for SQL Server}'
    
    print("🔌 Conectando a base de datos...")
    for server in servers:
        try:
            conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE=pasteleria_db;Trusted_Connection=yes;', timeout=1)
            print(f"✅ Conectado a: {server}")
            return conn
        except: continue
    print("❌ Error: No se encontró SQL Server")
    return None

# --- RUTAS ---
@app.route('/api/test', methods=['GET'])
def test_connection():
    """Ruta simple para probar que el servidor responde"""
    return jsonify({'status': 'ok', 'message': 'Servidor Python funcionando correctamente'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({'success': False, 'message': 'Error interno: No hay base de datos'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, rol, telefono FROM USUARIO WHERE email=? AND password=?", (data['email'], data['password']))
        user = cursor.fetchone()
        return jsonify({'success': True, 'user': {'id': user.id_usuario, 'nombre': user.nombre, 'rol': user.rol, 'telefono': user.telefono}}) if user else jsonify({'success': False, 'message': 'Datos incorrectos'})
    finally: conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    print(f"📝 Intentando registrar: {data['email']}") # Log para depurar
    conn = get_db_connection()
    if not conn: return jsonify({'success': False, 'message': 'Error de conexión con Base de Datos'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM USUARIO WHERE email = ?", (data['email'],))
        if cursor.fetchone(): return jsonify({'success': False, 'message': 'El correo ya existe'}), 400

        cursor.execute("INSERT INTO USUARIO (nombre, email, password, rol, telefono, estado) VALUES (?, ?, ?, 'cliente', ?, 1)", 
                      (data['nombre'], data['email'], data['password'], data['telefono']))
        conn.commit()
        print("✨ Usuario registrado con éxito")
        return jsonify({'success': True, 'message': 'Usuario registrado'})
    except Exception as e:
        print(f"❌ Error SQL: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally: conn.close()

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre, descripcion, precio_venta, imagen_url FROM PRODUCTO WHERE estado=1")
        products = [{'id': row.id_producto, 'nombre': row.nombre, 'desc': row.descripcion, 'precio': float(row.precio_venta), 'img': row.imagen_url or '🍰'} for row in cursor.fetchall()]
        return jsonify(products)
    finally: conn.close()

@app.route('/api/sales', methods=['POST'])
def create_sale():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({'success': False}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO VENTA (id_usuario, id_caja, subtotal, total, metodo_pago, cliente_nombre, fecha_venta) OUTPUT INSERTED.id_venta, INSERTED.fecha_venta VALUES (?, 1, ?, ?, 'efectivo', ?, GETDATE())", 
                      (data['vendedor_id'], data['total'], data['total'], data['cliente_nombre']))
        row = cursor.fetchone()
        
        for item in data['items']:
            cursor.execute("INSERT INTO DETALLE_VENTA (id_venta, id_producto, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)", (row.id_venta, item['id'], item['cant'], item['precio'], item['precio']*item['cant']))
            cursor.execute("UPDATE INVENTARIO SET stock_actual = stock_actual - ? WHERE id_producto = ?", (item['cant'], item['id']))
            
        codigo = f"B001-{str(row.id_venta).zfill(6)}"
        cursor.execute("INSERT INTO BOLETA (id_venta, numero_boleta, serie, nombre_cliente, estado) VALUES (?, ?, 'B001', ?, 'emitida')", (row.id_venta, codigo, data['cliente_nombre']))
        conn.commit()
        return jsonify({'success': True, 'boleta': codigo})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally: conn.close()

@app.route('/api/history', methods=['GET'])
def get_history():
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 20 v.id_venta, b.numero_boleta, v.cliente_nombre, v.total, v.fecha_venta, u.nombre FROM VENTA v JOIN BOLETA b ON v.id_venta = b.id_venta JOIN USUARIO u ON v.id_usuario = u.id_usuario ORDER BY v.fecha_venta DESC")
        return jsonify([{'id': r[0], 'codigo': r[1], 'cliente': r[2], 'total': float(r[3]), 'fecha': r[4].strftime('%Y-%m-%d %H:%M'), 'vendedor': r[5]} for r in cursor.fetchall()])
    finally: conn.close()

if __name__ == '__main__':
    print("\n🚀 SERVIDOR LISTO en http://127.0.0.1:5000")
    # host='0.0.0.0' permite que XAMPP o cualquier otra PC vea el servidor
    app.run(debug=True, host='0.0.0.0', port=5000)