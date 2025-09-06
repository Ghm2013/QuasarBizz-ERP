import flet as ft
import asyncio
from consultas import obtener_centros, insertar_usuario
import re

def efecto_hover(e):
    btn = e.control
    if e.data == "true":
        btn.bgcolor = "#FF3131" if btn.text == "Cancelar" else "#00ffaa"
        btn.scale = 1.02
    else:
        btn.bgcolor = "#EE4B2B" if btn.text == "Cancelar" else "#00cc88"
        btn.scale = 1
    btn.update()
def efecto_hover2(e):
    btn = e.control
    if e.data == "true":
        btn.bgcolor = "#438DF5" 
        btn.scale = 1.02
    else:
        btn.bgcolor = "#1418EE"
        btn.scale = 1
    btn.update()

def crear_formulario_newuser(page, on_guardar=None, on_cancelar=None, cargar_imagen=None):
    # Controles UI
    subtitulo = ft.Text("Crear nuevo usuario", size=40, color="grey70", opacity=0, animate_opacity=300)
    mensaje = ft.Text("", size=16, color="green70", opacity=0, animate_opacity=300,  max_lines = 3)

    campo_usuario = ft.TextField(
        label="Nombre y apellido",
        border_radius=15,
        border_color="grey70",
        color="grey70",
        focused_border_color="#00cc88",
        prefix=ft.Icon(ft.Icons.PERSON),
        opacity=0,
        animate_opacity=300,
    )

    campo_correo = ft.TextField(
        label="Correo Electrónico",
        border_radius=15,
        border_color="grey70",
        color="grey70",
        focused_border_color="#00cc88",
        prefix=ft.Icon(ft.Icons.MAIL),
        opacity=0,
        animate_opacity=300,
    )

    campo_contraseña = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        border_radius=15,
        border_color="grey70",
        color="grey70",
        
        focused_border_color="#00cc88",
        prefix=ft.Icon(ft.Icons.LOCK),
        opacity=0,
        animate_opacity=300,
    )

    campo_centro = ft.Dropdown(
        width=300,
        hint_text="Cargando áreas...",
        disabled=True,
        border_radius=15,
        border_color="grey70",
        color="grey70",
        focused_border_color="#00cc88",
        opacity=0,
        animate_opacity=300,
        options=[]
    )

    boton_guardar = ft.ElevatedButton(
        "Guardar Usuario",
        width=300,
        height=50,
        bgcolor="#00cc88",
        color="white",
        elevation=5,
        opacity=0,
        animate_opacity=300,
        animate_scale=300,
        on_hover=efecto_hover,
    )

    boton_cancelar = ft.ElevatedButton(
        "Cancelar",
        width=300,
        height=50,
        bgcolor="#EE4B2B",
        color="white",
        elevation=5,
        opacity=0,
        animate_opacity=300,
        animate_scale=300,
        on_hover=efecto_hover,
    )

    etiqueta_ruta_imagen = ft.Text(value="", visible=False)
    imagen_usuario = ft.Image(
        src="",
        width=250,
        height=250,
        border_radius=125,
        fit=ft.ImageFit.COVER,
        visible=False,
    )

    async def cargar_imagen(e: ft.FilePickerResultEvent):        
        if e.files:
            ruta = e.files[0].path
            etiqueta_ruta_imagen.value = ruta
            etiqueta_ruta_imagen.color = "white"
            etiqueta_ruta_imagen.visible = True
            imagen_usuario.src = ruta
            imagen_usuario.visible = True
            etiqueta_ruta_imagen.update()
            imagen_usuario.update()
            
    async def on_cargar_imagen_click(e):
        await asyncio.sleep(0.1)  # Espera breve para asegurar que el FilePicker ya fue agregado
        file_picker.pick_files(
            allow_multiple=False,
            file_type=[ft.FilePickerFileType.IMAGE],
        )

    file_picker = ft.FilePicker(on_result=cargar_imagen)
    page.overlay.append(file_picker)
    page.update()
    

    boton_cargar_imagen = ft.ElevatedButton(
        "Cargar Foto de Usuario",
        icon=ft.Icons.IMAGE,
        bgcolor="#1418EE",
        color="white",
        width=300,
        height=50,
        elevation=5,  
        opacity=0,
        animate_opacity=300,
        animate_scale=300, 
        on_hover=efecto_hover2,   
        on_click=lambda e: page.run_task(on_cargar_imagen_click, e) )    
        #on_click=lambda _: file_picker.pick_files(
        #    allow_multiple=False,
        #    file_type=[ft.FilePickerFileType.IMAGE],
        #),
        

    def guardar_interno(e, controles):  
        if e.control.text == "Nuevo Usuario":
            mensaje.value = ""
            mensaje.color = "orange"
            mensaje.update()
            e.control.text = "Guardar Usuario"
            e.control.disabled = False
            e.control.update()
            return

        e.control.disabled = True
        e.control.text = "Guardando..."
        e.control.update()

        nombre = controles["campo_usuario"].value.strip()
        correo = controles["campo_correo"].value.strip()
        contraseña = controles["campo_contraseña"].value.strip()
        centro_id = controles["campo_centro"].value
        ruta_imagen = controles["ruta_imagen"].value.strip()

        if not nombre or not correo or not contraseña or not centro_id:
            mensaje.value = "⚠️ Todos los campos son obligatorios."
            mensaje.color = "orange"
            mensaje.update()
            e.control.text = "Guardar Usuario"
            e.control.disabled = False
            e.control.update()
            return
        if not es_correo_valido(correo):
            mensaje.value = "⚠️ Ingresa un correo electrónico válido."
            mensaje.color = "orange"
            mensaje.update()
            e.control.text = "Guardar Usuario"
            e.control.disabled = False
            e.control.update()
            return
        
        respuesta = insertar_usuario(nombre, correo, contraseña, centro_id, ruta_imagen)  # Puedes incluir ruta_imagen si lo necesitas
        if respuesta[1] == 1:
            mensaje.value = "✅ Usuario guardado exitosamente."
            mensaje.color = "green"
        else:
            mensaje.value = respuesta[0]
            mensaje.color = "orange"

        mensaje.update()

        if respuesta[1] == 1:
            for campo in ["campo_usuario", "campo_correo", "campo_contraseña", "campo_centro"]:
                controles[campo].value = "" if campo != "campo_centro" else None
                controles[campo].update()
            controles["ruta_imagen"].value = ""
            controles["ruta_imagen"].visible = False
            controles["imagen_usuario"].src = ""
            controles["imagen_usuario"].visible = False
            controles["ruta_imagen"].update()
            controles["imagen_usuario"].update()

        e.control.text = "Nuevo Usuario"
        e.control.disabled = False
        e.control.update()
        
    def es_correo_valido(correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(patron, correo) is not None
    
    def handle_guardar(e):
        controles = {
            "campo_usuario": campo_usuario,
            "campo_correo": campo_correo,
            "campo_contraseña": campo_contraseña,
            "campo_centro": campo_centro,
            "mensaje": mensaje,
            "ruta_imagen": etiqueta_ruta_imagen,
            "imagen_usuario": imagen_usuario,
        }

        if on_guardar:
            on_guardar(e, controles)
        else:
            guardar_interno(e, controles)

    boton_guardar.on_click = handle_guardar
    if on_cancelar:
        boton_cancelar.on_click = on_cancelar

    columna_formulario = ft.Column(
        [
            ft.Row([ft.Icon(ft.Icons.SUPERVISED_USER_CIRCLE_ROUNDED, size=50, color="#00cc88")], alignment="right"),
            subtitulo,
            mensaje,
            ft.Divider(height=20, color="transparent"),
            campo_usuario,
            campo_correo,
            campo_contraseña,
            campo_centro,
            ft.Divider(height=20, color="transparent"),
            boton_guardar,
            boton_cancelar,
        ],
        horizontal_alignment="center",
        spacing=10
    )

    columna_imagen = ft.Column(
        [
            boton_cargar_imagen,
            imagen_usuario,
            etiqueta_ruta_imagen,
        ],
        horizontal_alignment="center",
        spacing=20
    )

    contenedor_login = ft.Container(
        width=900,
        height=700,
        padding=40,
        border_radius=20,
        bgcolor="#FFFFFF",
        border=ft.border.all(2, "#00cc88"),
        animate=ft.Animation(500, "easeOut"),
        content=ft.Row(
            [
                columna_formulario,
                columna_imagen
            ],
            alignment="spaceBetween",
            vertical_alignment="start",
        ),
    )

    async def animar_y_cargar():
        await asyncio.sleep(0.5)
        for control in [subtitulo, mensaje, campo_usuario, campo_correo, campo_contraseña, campo_centro]:
            control.opacity = 1
            control.update()
        await asyncio.sleep(0.3)
        boton_guardar.opacity = 1
        boton_cancelar.opacity = 1
        boton_cargar_imagen.opacity = 1
        boton_guardar.update()
        boton_cancelar.update()
        boton_cargar_imagen.update()

        try:
            resultados = obtener_centros()
            campo_centro.options = [
                ft.dropdown.Option(key=str(id), text=nombre)
                for id, nombre in resultados
            ]
            campo_centro.hint_text = "Selecciona un área"
            campo_centro.disabled = False
        except Exception as ex:
            campo_centro.hint_text = f"Error al cargar: {str(ex)}"
        finally:
            campo_centro.update()

    page.run_task(animar_y_cargar)

    return {
        "container": contenedor_login,
        "cargar_centros": lambda: page.run_task(animar_y_cargar)
    }
