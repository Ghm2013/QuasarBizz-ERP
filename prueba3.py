import flet as ft
import asyncio
from consultas import login
from main import main_app


# Efecto hover para el botón
def efecto_hover(e):
    btn = e.control
    if e.data == "true":
        if btn.text == "Cancelar":
            btn.bgcolor = "#FF3131"
        else:
            btn.bgcolor = "#00ffaa"
        btn.scale = 1.02
    else:
        if btn.text == "Cancelar":
            btn.bgcolor = "#EE4B2B"
        else:
            btn.bgcolor = "#00cc88"
        btn.scale = 1
    btn.update()


async def login_main(page: ft.Page):
    # Configuración básica de la página
    page.title = "Login Animado"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = "#1a1a2e"
    page.padding = 10


    # Elementos de la interfaz
    titulo = ft.Text(
        "Bienvenido",
        size=40,
        weight="bold",
        color="white",
        opacity=0,
        animate_opacity=300,
    )

    subtitulo = ft.Text(
        "Inicia sesión para continuar",
        size=16,
        color="white70",
        opacity=0,
        animate_opacity=300,
    )

    mensaje_error = ft.Text(
        "",
        size=14,
        color="#FF5555",
        opacity=0,
        animate_opacity=300,
    )

    campo_usuario = ft.TextField(
        label="Correo Electrónico",
        border_radius=15,
        border_color="white70",
        color="white",
        focused_border_color="#00cc88",
        prefix=ft.Icon(ft.Icons.PERSON),
        opacity=0,
        animate_opacity=300,
    )

    campo_password = ft.TextField(
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

    boton_login = ft.ElevatedButton(
        "Iniciar Sesión",
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

    # Contenedor principal
    contenedor_login = ft.Container(
        width=400,
        padding=40,
        border_radius=20,
        bgcolor="#16213e",
        border=ft.border.all(2, "#00cc88"),
        animate=ft.Animation(500, "easeOut"),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(
                            src="/assets/iconos/QuasarBizz_ERP-amplio.png",
                            width=200,
                            height=80,
                        )
                    ],
                    alignment="center",
                ),
                titulo,
                subtitulo,
                mensaje_error,
                ft.Divider(height=20, color="transparent"),
                campo_usuario,
                campo_password,
                ft.Divider(height=20, color="transparent"),
                boton_login,
                boton_cancelar,
            ],
            horizontal_alignment="center",
        ),
    )

    # Animación de entrada
    async def animar_entrada():
        await asyncio.sleep(0.5)
        titulo.opacity = 1
        subtitulo.opacity = 1
        campo_usuario.opacity = 1
        campo_password.opacity = 1
        page.update()

        await asyncio.sleep(0.3)
        boton_login.opacity = 1
        boton_cancelar.opacity = 1
        page.update()

    # Función para manejar el login
    async def login_click(e):
        email = campo_usuario.value.strip()
        password = campo_password.value

        if not email or not password:
            mensaje_error.value = "Por favor complete todos los campos"
            mensaje_error.opacity = 1
            mensaje_error.update()
            return

        boton_login.disabled = True
        boton_login.text = "Iniciando..."
        boton_login.update()

        try:
            await asyncio.sleep(0.7)  # Simulación de red
            resultado = login(email, password)

            if resultado[0] == 4:
                mensaje_error.value = "EL Usuario tiene una Sesión activa"
                mensaje_error.color = "yellow"
                mensaje_error.opacity = 1
                mensaje_error.update()
                return

            if isinstance(resultado, tuple) and resultado[1] == 1:
                # Si el login es exitoso
                page.clean()
                # En navegador no hay window, así que solo carga main_app
                main_app(page, resultado[1], resultado[0], resultado[2])
                page.update()
            elif resultado[0] == 2:
                mensaje_error.value = "Usuario o Contraseña Incorrectos"
                mensaje_error.color = "red"
                mensaje_error.opacity = 1
                mensaje_error.update()
            else:
                mensaje_error.value = "Error al hacer la consulta a la base de datos"
                mensaje_error.color = "red"
                mensaje_error.opacity = 1
                mensaje_error.update()

        except Exception as ex:
            mensaje_error.value = f"Error: {str(ex)}"
            mensaje_error.opacity = 1
            mensaje_error.update()
        finally:
            boton_login.disabled = False
            boton_login.text = "Iniciar Sesión"
            boton_login.update()

    def cancelar_click(e):
        if campo_password.value or campo_usuario.value:
            campo_password.value = ""
            campo_usuario.value = ""
            campo_usuario.update()
            campo_password.update()
            mensaje_error.value = ""
            mensaje_error.opacity = 0
            mensaje_error.update()
        else:
            # En navegador no se puede cerrar ventana -> limpiamos la página
            page.clean()
            page.add(ft.Text("Sesión cancelada", color="white"))

    # Configurar eventos
    boton_login.on_click = login_click
    boton_cancelar.on_click = cancelar_click

    # Añadir todo a la página
    page.add(contenedor_login)

    # Lanzar animación con run_task (más seguro en web)
    page.run_task(animar_entrada)


# Ejecutar en el navegador web
ft.app(target=login_main, view=ft.WEB_BROWSER, port=8000)
