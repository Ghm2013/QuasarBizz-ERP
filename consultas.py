
from database import get_connection
import bcrypt
import flet as ft
import os
import shutil


def insertar_usuario(usuario, correo,contraseña, departamento, foto):
    hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = get_connection()
        cursor = conn.cursor()
        #Verificar si ya existe un usuario con mismo nombre y correo
        cursor.execute("""
            SELECT COUNT(*) FROM usuarios
            WHERE nombre_usuario = ? AND correo = ?;
        """, (usuario, correo))
        resultado = cursor.fetchone()
        if resultado and resultado[0] is not None:
            existe = resultado[0]
        else:
            existe = 0  # Asumimos que no hay coincidencias
                
        if existe > 0:
            mensaje =["⚠️ Ya existe un usuario con el nombre '{}' y correo '{}'.".format(usuario,correo),2]
            return mensaje 
        
        check_foto = copiar_imagen_a_assets(foto)
        if check_foto[1] == 1:
            cursor.execute("""
                INSERT INTO usuarios (nombre_usuario, correo, pass, departamento, foto)
            VALUES (?, ?, ?, ?, ?);
            """, (usuario, correo, hashed_password.decode('utf-8'), departamento, check_foto[0]))
            conn.commit()
            mensaje=["✅ Usuario '{}' insertado correctamente.".format(usuario),1]       
            return mensaje
        else:
            mensaje=[f"❌ Error al insertar usuario, Comuniquese con el administrador del sistema",2]
            #print (e)
            return mensaje
            
    
    except Exception as e:
        mensaje=[f"❌ Error al insertar usuario, Comuniquese con el administrador del sistema",2]
        print (e)
        return mensaje
    finally:
        conn.close()
def copiar_imagen_a_assets(ruta_origen: str):
    if not ruta_origen or not os.path.isfile(ruta_origen):
        print("⚠️ Ruta de imagen inválida o archivo no encontrado.")
        return

    carpeta_destino = "assets/fotos"
    os.makedirs(carpeta_destino, exist_ok=True)

    nombre_archivo = os.path.basename(ruta_origen)
    ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
    

    try:
        shutil.copy(ruta_origen, ruta_destino)
        #print(f"✅ Imagen copiada a: {ruta_destino}")
        chequeo = (ruta_destino,1)
        return chequeo
    
    except Exception as e:
        chequeo = (0,0)
        return chequeo
        #print(f"❌ Error al copiar la imagen: {e}")

def obtener_productos_cc():
    pass
        
def obtener_centros():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idcentro, descripcion FROM centros ORDER BY descripcion ASC")
        resultados = cursor.fetchall()
        return resultados
    except Exception as ex:
        raise Exception(f"Error al obtener centros: {ex}")
    finally:
        if 'conn' in locals():
            conn.close()
            
            
def login(usuario, password):
    correo_limpio = usuario.strip().lower()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE LOWER(TRIM(correo)) = ?;', (correo_limpio,))
        result = cursor.fetchone()
        
        if result[5]== 1:
            return (4,4)


         # result[2] asumo es el campo contraseña hasheada (ajusta índice si es otro)
        password_hash_db = result[3] 
        
        if isinstance(password_hash_db, str):
            password_hash_db = password_hash_db.encode('utf-8')  # convierte string a bytes
            

        # Verifica contraseña
        if bcrypt.checkpw(password.encode('utf-8'), password_hash_db):
            # Contraseña correcta, actualizar estado = 1
            cursor.execute('UPDATE usuarios SET estado = 1 WHERE LOWER(TRIM(correo)) = ?;', (correo_limpio,))
            conn.commit()
            return (result[1], 1,result[2],result[6])  # ejemplo, devuelvo usuario y código éxito
        else:
            # Contraseña incorrecta
            return (2, 2)

    except Exception as e:
        resultado = 3
        return resultado

    finally:
        conn.close()
        
def cerrar_sesion(correo):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET estado = 0 WHERE LOWER(TRIM(correo)) = ?;', (correo,))
        conn.commit()
        
        result = (0,0,None)
        return result
    except Exception as e:
        result = ("Error al cerrar sesión", 1, e)
        print ("Esto tiene Result: " + result[1])
        return result
    finally:
        conn.close()
        
def obtener_productos(categoria):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT codigo, nombre, unidad_de_medida FROM Productos WHERE categoria = ? ORDER BY nombre ASC;", (categoria,) )
    resultados = cursor.fetchall()
    
    conn.close()
    return resultados

def obtener_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM categoria;")
    resultados = cursor.fetchall()
    
    conn.close()
    return resultados

def obtener_descripcion_unidad(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT  nombre, unidad_de_medida FROM Productos WHERE codigo = ? ORDER BY nombre ASC;", (codigo,) )
    resultados = cursor.fetchall()    
    
    conn.close()
    return resultados

def logout_forzado(user_id):
    # Aquí haces tu UPDATE a la base de datos:
    # UPDATE usuarios SET activo = 0 WHERE id = user_id
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET estado = 0 WHERE LOWER(TRIM(correo)) = ?;', (user_id,))
    conn.commit()
    conn.close()
    
def obtener_productos_cc(categoria_id, centro_id):
    # Aquí iría el código para obtener los productos
    # filtrando por categoria_id y centro_id
    # Por ejemplo, una consulta a una base de datos
    # y devolver la lista de productos
    pass