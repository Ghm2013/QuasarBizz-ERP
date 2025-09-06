import flet as ft
import datetime
from consultas import obtener_centros, obtener_categorias, obtener_productos_cc
from imprimir_oc import generar_consolidado_pdf
import locale

def crear_formulario_consol_solicitud(page):
    # Configurar el locale a nivel de la página para los controles de Flet
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[ft.Locale("es", "ES")],
        current_locale=ft.Locale("es", "ES")
    )
    # Establecer el locale a español para el formato de fecha
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        # Manejar el caso si 'es_ES.UTF-8' no está disponible (ej. en Windows)
        locale.setlocale(locale.LC_TIME, 'es_ES')    
    
    fecha_actual = datetime.datetime.now().date()
    productos_cantidad_fields = []

    ck_todos_cc = ft.Checkbox(label= "Todos los Centros de Costos", animate_size= 12)

    fecha_sol = ft.Text(fecha_actual.strftime('%B %Y'), size=18, weight=ft.FontWeight.BOLD, color="BLUE")
    def handle_change(e):
        # Actualiza el texto con la fecha seleccionada
        fecha_sol.value = e.control.value.strftime('%B %Y')
        fecha_sol.update()

    def handle_dismissal(e):
        # Puedes manejar evento si se cierra el DatePicker sin seleccionar fecha
        pass

    def open_date_picker(e):
        page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2025, month=1, day=1),
                last_date=datetime.datetime(year=2030, month=12, day=1),
                value=datetime.datetime.now(),
                on_change=handle_change,
                on_dismiss= handle_dismissal
            )
        )

    tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Código")),
                ft.DataColumn(label=ft.Text("Descripción")),
                ft.DataColumn(label=ft.Text("Unidad")),
                ft.DataColumn(label=ft.Text("Cantidad")),
                    ],
            rows=[]
            )

    dropdown_categoria = ft.Dropdown(
                                        label="Categoría",
                                        width=250,
                                        text_style=ft.TextStyle(
                                                size=14,
                                                color=ft.Colors.BLACK
                                                ),
                                        bgcolor=ft.Colors.GREY_200
                                    )

    dropdown_centros = ft.Dropdown(label="Centro de Costo",
                                    width=250,
                                    text_style=ft.TextStyle(
                                                size=14,
                                                color=ft.Colors.BLACK
                                        ),
                                    bgcolor=ft.Colors.GREY_200)

    # Se mueve la inicialización del contenedor aquí
    contenedor = ft.Container(
        expand=True,
        padding=40,
        border_radius=20,
        bgcolor="#FFFFFF",
        border=ft.border.all(2, "#00cc88"),
        animate=ft.Animation(500, "easeOut"),
        content=None # Se inicializa con None
        )

    def construir_tabla(productos):
        """productos_cantidad_fields.clear()
        filas = []
        for codigo, descripcion, unidad in productos:
            tf_cantidad = ft.TextField(value="", width=100)
            productos_cantidad_fields.append((codigo, tf_cantidad))
            fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(codigo)),
                ft.DataCell(ft.Text(descripcion)),
                ft.DataCell(ft.Text(unidad)),
                ft.DataCell(tf_cantidad),
                ]
            )
        filas.append(fila)
        tabla.rows = filas
        tabla.update()
        # Ahora contenedor ya no es None, se puede actualizar
        if contenedor is not None:
            contenedor.update()"""
        pass

    def on_categoria_change(e):
        categoria_id = dropdown_categoria.value
        centro_id = dropdown_centros.value
        if categoria_id and centro_id:
            productos = obtener_productos_cc(categoria_id, centro_id)
            construir_tabla(productos)

    def on_centros_change(e):
        categoria_id = dropdown_categoria.value
        centro_id = dropdown_centros.value
        if categoria_id and centro_id:
            productos = obtener_productos_cc(categoria_id, centro_id)
            construir_tabla(productos)

    def on_imprimir_solicitud(e):
        generar_consolidado_pdf(tabla, fecha_sol)

    # Obtener categorías
    categorias = obtener_categorias()
    dropdown_categoria.options = [
        ft.dropdown.Option(str(cat_id), text=nombre) for cat_id, nombre in categorias
        ]
    dropdown_categoria.on_change = on_categoria_change

    centros = obtener_centros()
    dropdown_centros.options = [
        ft.dropdown.Option(str(id_centro), text=descripcion) for id_centro, descripcion in centros
        ]
    dropdown_categoria.on_change = on_categoria_change
    dropdown_centros.on_change = on_centros_change
    # Establecer valor por defecto, sin construir aún
    if categorias:
        dropdown_categoria.value = str(categorias[0][0])
    if centros:
        dropdown_centros.value = str(centros[0][0])

    # TAB Solicitud de compra
    tab_solicitud = ft.Container(
        padding=10,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Container(
                    height=80,
                    alignment=ft.alignment.center_left,
                    content=ft.Row(
                    controls=[
                            #ft.Text(
                            #    "Fecha:",
                            #    size=14,
                            #    weight=ft.FontWeight.BOLD,
                            #    color=ft.Colors.BLUE
                            #),
                            fecha_sol,
                            ft.ElevatedButton(
                                 "Elegir Mes",
                                width=150,
                                height=50,
                                color=ft.Colors.WHITE,
                                icon=ft.Icons.CALENDAR_MONTH,
                                bgcolor=ft.Colors.YELLOW_700,
                                on_click=open_date_picker,
                                style=ft.ButtonStyle(
                                padding=10,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                                    )
                            ),
                            dropdown_categoria,
                            dropdown_centros,
                            ck_todos_cc,
                            
                            ft.ElevatedButton(
                                "Imprimir",
                                width=150,
                                height=50,
                                on_click=on_imprimir_solicitud,
                                icon=ft.Icons.SAVE,
                                bgcolor=ft.Colors.GREEN,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                padding=10,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                                    )
                            )
                         ]
                    )
                ),
                tabla
            ],
            scroll="auto"
        )
    )

    contenedor.content = tab_solicitud

    # Devolver el contenedor y el evento de carga inicial
    return {
        "container": contenedor,
        "dropdown_event": lambda e=None: on_categoria_change(e)
    }
