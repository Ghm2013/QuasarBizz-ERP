import flet as ft
import datetime
from consultas import obtener_productos, obtener_categorias, obtener_descripcion_unidad
from imprimir_oc import generar_pdf

def crear_formulario_sol_compra(page):
    fecha_actual = datetime.datetime.now().date()
    productos_cantidad_fields = []
    # Campos para ingresar productos manualmente
    codigo_tf = ft.TextField(label="Código", width=100)
    descripcion_tf = ft.TextField(label="Descripción", width=200, read_only=True)
    unidad_tf = ft.TextField(label="Unidad", width=100, read_only=True)
    cantidad_tf = ft.TextField(label="Cantidad", width=100)
    precio_tf = ft.TextField(label="Precio Unit", width=100) 
    total_tf = ft.TextField(label="Total", width=100, read_only = True)
    checkbox_1 = ft.Checkbox(label="Exento")
    sub_total_oc = ft.Text("0.00", width=100, color="GREEN", weight=ft.FontWeight.BOLD)
    iva_oc = ft.Text("0.00", width=100, color="GREEN", weight=ft.FontWeight.BOLD)
    total_oc = ft.Text("0.00", width=100, color="GREEN", weight=ft.FontWeight.BOLD)
    proveedor_tf = ft.TextField(label="Proveedor", width=250, read_only= True )
    ruc_tf = ft.TextField(label="RUC", width=150)
    moneda_oc =  ft.Dropdown(
        label="Selecciona una moneda",
        options=[
            ft.dropdown.Option("Córdobas"),
            ft.dropdown.Option("Dólares"),
        ],
        width=200
    )
    fecha_oc = ft.Text(fecha_actual.strftime('%d/%m/%Y'), size=18, weight=ft.FontWeight.BOLD, color="BLUE")
    def handle_change(e):
        # Actualiza el texto con la fecha seleccionada
        fecha_oc.value = e.control.value.strftime('%d/%m/%Y')
        fecha_oc.update()

    def handle_dismissal(e):
        # Puedes manejar evento si se cierra el DatePicker sin seleccionar fecha
        pass

    def open_date_picker(e):
        page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2000, month=10, day=1),
                last_date=datetime.datetime(year=2025, month=10, day=1),
                value=datetime.datetime.now(),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
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
    
    dropdown_categoria = ft.Dropdown(label="Categoría",
                                     width=250,
                                        text_style=ft.TextStyle(
                                            size=14,
                                            color=ft.Colors.BLACK
                                        ),
                                        bgcolor=ft.Colors.GREY_200)

    # Aquí declaramos contenedor como None para luego actualizarlo en construir_tabla
    contenedor = None
    


    def construir_tabla(productos):
        productos_cantidad_fields.clear()
        filas = []
        for codigo, descripcion, unidad in productos:
                tf_cantidad = ft.TextField(value="", width=100)
                productos_cantidad_fields.append((codigo, tf_cantidad))  # Guardar código y campo
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
        # Actualizar el contenedor para refrescar la UI
        if contenedor is not None:
            contenedor.update()

        
    # Evento para cuando se hace enter o pierde foco en codigo_tf
    def codigo_tf_changed(e):
        codigo = codigo_tf.value.strip().upper()  # ✅ corregido, no se llama como función

        resultado = obtener_descripcion_unidad(codigo)

        if resultado and isinstance(resultado[0], tuple) and len(resultado[0]) == 2:
            descripcion_tf.value = resultado[0][0]
            unidad_tf.value = resultado[0][1]
        else:
            descripcion_tf.value = ""
            unidad_tf.value = ""

        descripcion_tf.update()
        unidad_tf.update()
        
        # Asignar eventos a codigo_tf
    codigo_tf.on_submit = codigo_tf_changed
    codigo_tf.on_blur = codigo_tf_changed 
    
        
    def on_categoria_change(e):
        categoria_id = dropdown_categoria.value
        if categoria_id:
            productos = obtener_productos(categoria_id)
            construir_tabla(productos)

    def on_guardar_solicitud(e):
        datos = [(codigo, tf.value) for codigo, tf in productos_cantidad_fields]
        print("Datos capturados (código, cantidad):", datos)
        # Aquí puedes hacer algo con esos datos, por ejemplo filtrarlos:
        datos_validos = [(c, q) for c, q in datos if q.strip() != ""]
        print("Solo datos válidos:", datos_validos)


        
    def imprimir_tabla_oc(e):
        pass
        #generar_pdf(tabla_oc, proveedor_tf, ruc_tf, fecha_oc,sub_total_oc, iva_oc, total_oc)

    # Obtener categorías
    categorias = obtener_categorias()
    dropdown_categoria.options = [
        ft.dropdown.Option(str(cat_id), text=nombre) for cat_id, nombre in categorias
    ]
    dropdown_categoria.on_change = on_categoria_change

    # Establecer valor por defecto, sin construir aún
    if categorias:
        dropdown_categoria.value = str(categorias[0][0])

    # TAB Solicitud de compra
    tab_solicitud = ft.Container(
        # Quitamos height para que ajuste según contenido
        #width=950,
        padding=10,
        expand= True,
         content=ft.Column(
                    controls=[
                        ft.Container(  # Solo esta parte tiene altura fija
                            height=80,
                            alignment=ft.alignment.center_left,
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y')}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE
                                    ),
                                    dropdown_categoria,
                                    ft.ElevatedButton(
                                        "Guardar",
                                        width=150,  # ancho en píxeles
                                        height=50,  # alto en píxeles
                                        on_click=on_guardar_solicitud,
                                        icon = ft.Icons.SAVE,
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
                        tabla  # La tabla no se ve afectada por el alto del contenedor superior
                    ],
                    scroll="auto"  # Esto permite scroll si el contenido crece
                )
    )

   

    # TAB Solicitud de pago
    tab_solicitud_pago = ft.Container(
        #width=950,
        padding=10,
        expand=True,
        content=ft.Column([
            ft.Text("Configuración", size=18, weight=ft.FontWeight.BOLD),
            ft.Switch(label="Activar cuenta"),
            ft.Dropdown(label="Rol", options=[
                ft.dropdown.Option("Administrador"),
                ft.dropdown.Option("Usuario"),
                ft.dropdown.Option("Invitado")
            ]),
            ft.ElevatedButton("Guardar", on_click=lambda e: print("Guardar configuración"))
        ],
            scroll="auto"  # <--- Esto habilita scroll vertical si se necesita
            )
    )

    # TABS
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Solicitud de Compra", content=tab_solicitud),
            ft.Tab(text="Solicitud de pago", content=tab_solicitud_pago)
        ],
        expand=True
    )
    
    # CONTENEDOR PRINCIPAL - simplificado para que las tabs ocupen todo el espacio
    contenedor = ft.Container(
        expand= True,
        #width=1000,
        #height=650,  # Ajustamos altura para que contenga todo sin recorte
        padding=40,
        border_radius=20,
        bgcolor="#FFFFFF",
        border=ft.border.all(2, "#00cc88"),
        animate=ft.Animation(500, "easeOut"),
        content=tab_solicitud  # Directamente las tabs sin Rows ni Columns extras
    )
       
    # Devolver el contenedor y el evento de carga inicial
    return {
        "container": contenedor,
        "dropdown_event": lambda e=None: on_categoria_change(e)
    }
