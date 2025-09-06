import flet as ft
import asyncio
from consultas import obtener_centros, insertar_usuario

# Efecto hover para el botón
def efecto_hover(e):
    btn = e.control
    if e.data == "true":
        btn.bgcolor = "#FF3131" if btn.text == "Cancelar" else "#00ffaa"
        btn.scale = 1.02
    else:
        btn.bgcolor = "#EE4B2B" if btn.text == "Cancelar" else "#00cc88"
        btn.scale = 1
    btn.update()

def crear_formulario(page, on_guardar=None, on_cancelar=None):
    # Controles UI
    titulo = ft.Text("Bienvenido", size=40, weight="bold", color="white", opacity=0, animate_opacity=300)
    subtitulo = ft.Text("Crear nuevo usuario", size=16, color="white70", opacity=0, animate_opacity=300)
    mensaje = ft.Text("", size=16, color="green70", opacity=0, animate_opacity=300)

    campo_usuario = ft.TextField(
        label="Nombre y apellido",
        border_radius=15,
        border_color="white70",
        color="white",
        focused_border_color="#00cc88",
        prefix=ft.Icon(ft.Icons.PERSON),
        opacity=0,
        animate_opacity=300,
    )

    campo_correo = ft.TextField(
        label="Correo Electrónico",
        border_radius=15,
        border_color="white70",
        color="white",
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
        border_color="white70",
        color="white",
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
        border_color="white70",
        color="white",
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

    def handle_guardar(e):
        datos_usuario = {
            "campo_usuario": campo_usuario,
            "campo_correo": campo_correo,
            "campo_contraseña": campo_contraseña,
            "campo_centro": campo_centro,
            "mensaje": mensaje,
        }
        if on_guardar:
            on_guardar(e, datos_usuario)

    boton_guardar.on_click = handle_guardar

    if on_cancelar:
        boton_cancelar.on_click = on_cancelar

    contenedor_login = ft.Container(
        width=450,
        padding=40,
        border_radius=20,
        bgcolor="#16213e",
        border=ft.border.all(2, "#00cc88"),
        animate=ft.animation.Animation(500, "easeOut"),
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color="#00cc88")], alignment="center"),
                titulo,
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
        ),
    )

    async def animar_y_cargar():
        await asyncio.sleep(0.5)
        for control in [titulo, subtitulo, mensaje, campo_usuario, campo_correo, campo_contraseña, campo_centro]:
            control.opacity = 1
            control.update()

        await asyncio.sleep(0.3)
        boton_guardar.opacity = 1
        boton_cancelar.opacity = 1
        boton_guardar.update()
        boton_cancelar.update()

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
        "controls": {
            "campo_usuario": campo_usuario,
            "campo_correo": campo_correo,
            "campo_contraseña": campo_contraseña,
            "campo_centro": campo_centro,
            "mensaje": mensaje,
        }
    }

def main(page: ft.Page):
    page.title = "Login Animado"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window.center()
    page.bgcolor = "#1a1a2e"
    page.padding = 20
    page.window.title_bar_hidden = True
    page.window.frameless = True
    page.window.width = 400
    page.window.height = 750

    def guardar_click(e, controls):
        
        #Verificar que no haya un usario guardado anteriormente 
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

        nombre = controls["campo_usuario"].value.strip()
        correo = controls["campo_correo"].value.strip()
        contraseña = controls["campo_contraseña"].value.strip()
        centro_id = controls["campo_centro"].value
        mensaje = controls["mensaje"]

        # Validar campos vacíos
        if not nombre or not correo or not contraseña or not centro_id:
            mensaje.value = "⚠️ Todos los campos son obligatorios."
            mensaje.color = "orange"
            mensaje.update()
            e.control.text = "Guardar Usuario"
            e.control.disabled = False
            e.control.update()
            return

        # Guardado uardado
        respuesta= insertar_usuario( nombre, correo, contraseña, centro_id)
        if respuesta[1] == 1:
            mensaje.value = "✅ Usuario guardado exitosamente."
            mensaje.color = "green"
            mensaje.update()
            e.control.text = "Nuevo Usuario"
            e.control.disabled = False
            e.control.update()
            
        elif respuesta[1] == 2:
            mensaje.value = respuesta[0]
            mensaje.color = "orange"
            mensaje.update()
            e.control.text = "Guardar Usuario"
            e.control.disabled = False
            e.control.update()
            return  
        
        

        # Limpiar campos
        controls["campo_usuario"].value = ""
        controls["campo_correo"].value = ""
        controls["campo_contraseña"].value = ""
        controls["campo_centro"].value = None

        for campo in ["campo_usuario", "campo_correo", "campo_contraseña", "campo_centro"]:
            controls[campo].update()

        e.control.text = "Guardar Usuario"
        e.control.disabled = False
        e.control.update()

    def cancelar_click(e):
        page.window.close()

    form = crear_formulario(page, on_guardar=guardar_click, on_cancelar=cancelar_click)
    page.add(form["container"])


