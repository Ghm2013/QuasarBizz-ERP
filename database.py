import sqlitecloud

def get_connection():
    # Abrir la conexión a SQLite Cloud
    return sqlitecloud.connect("sqlitecloud://cde41vaahz.g4.sqlite.cloud:8860/erp_data?apikey=e905VtCKnqw5IlLHfr1xTslthq1RUd9AmL6mb01TtnA")
                                
def crear_tabla_productos():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Productos (
            Codigo TEXT,
            nombre TEXT,
            Unidad_de_medida TEXT,
            categoria INTEGER,
            FOREIGN KEY (categoria) REFERENCES categoria(idcategoria)
        );
    """)
    print("Tabla 'Productos' creada correctamente.")
    conn.close()

def crear_tabla_categoria():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            idcategoria INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT
        );
    """)
    print(" Tabla 'categoria' creada correctamente.")
    conn.close()
    
def crear_tabla_usuario():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario Text,            
            correo TEXT,
            pass Text,
            departamento INTEGER,
            FOREIGN KEY (departamento) REFERENCES centros(idcentro)
        );
    """)
    print(" Tabla 'USUARIOS' creada correctamente.")
    conn.close()

def crear_tabla_centro_costo():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS centros (
            idcentro INTEGER PRIMARY KEY,
            descripcion TEXT
        );
    """)
    print(" Tabla 'centros' creada correctamente.")
    conn.close()
    
def crear_tabla_cuentas():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cuentas (
            idcuenta INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT
        );
    """)
    print(" Tabla 'Cuentas' creada correctamente.")
    conn.close()
    
def crear_relacion_producto_categoria():
    conn = get_connection()
    #1. Crear copia temporal de empleados
    conn.execute("""
                 CREATE TABLE productos_temp AS SELECT * FROM Productos;""")

    #2. Recrear la tabla con FOREIGN KEY
    conn.execute("""
                 DROP TABLE Productos;""")

    conn.execute("""
                 CREATE TABLE Productos (
                Codigo TEXT,
            nombre TEXT,
            Unidad_de_medida TEXT,
            categoria INTEGER,
        FOREIGN KEY (categoria) REFERENCES categoria(idcategoria)
         );""")

        #3. Migrar los datos
    conn.execute("""
                     INSERT INTO Productos SELECT * FROM productos_temp;
        DROP TABLE productos_temp;""")
    print(" Clave foranea creada correctamente.")
    conn.close()

   
def crear_relacion_usuarios_centros():
    conn = get_connection()
    #1. Crear copia temporal de empleados
    conn.execute("""
                 CREATE TABLE usuarios_temp AS SELECT * FROM usuarios;""")

    #2. Recrear la tabla con FOREIGN KEY
    conn.execute("""
                 DROP TABLE usuarios;""")

    conn.execute("""
                 CREATE TABLE usuarios (
                idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario Text,            
            correo TEXT,
            pass Text,
            departamento INTEGER,
        FOREIGN KEY (departamento) REFERENCES centros(idcentro)
         );""")

        #3. Migrar los datos
    conn.execute("""
                     INSERT INTO usuarios SELECT * FROM usuarios_temp;
        DROP TABLE usuarios_temp;""")
    print(" Clave foranea creada correctamente.")
    conn.close()

    

# Ejecutar la función si este archivo se ejecuta directamente
if __name__ == "__main__":
    crear_tabla_productos()
    crear_tabla_categoria()
    crear_tabla_usuario()
    crear_tabla_centro_costo()
    crear_tabla_cuentas()
    #crear_relacion_producto_categoria()
    #crear_relacion_usuarios_centros()
    