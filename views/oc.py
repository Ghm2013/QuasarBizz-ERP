import flet as ft
import datetime
from consultas import obtener_productos, obtener_categorias, obtener_descripcion_unidad
from imprimir_oc import generar_pdf

def crear_formulario_oc(page):
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
    tabla_oc = ft.DataTable(
        columns=[
            
            ft.DataColumn(label=ft.Text("Código")),
            ft.DataColumn(label=ft.Text("Descripción")),
            ft.DataColumn(label=ft.Text("Unidad")),
            ft.DataColumn(label=ft.Text("Cantidad")),
            ft.DataColumn(label=ft.Text("Precio Unit.")),
            ft.DataColumn(label=ft.Text("Total")),
            ft.DataColumn(label=ft.Text("Exento")),
            ft.DataColumn(label=ft.Text("Eliminar")),
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
        
        # Actualizar el contenedor para refrescar la UI
        if contenedor is not None:
            contenedor.update()
            #tabla.update()
    # Función de manejo del checkbox
    def checkbox_changed(e):
        #fila = e.control.data
        recalcular_totales()
        #print(f"Checkbox fila {fila} = {e.control.value}")
        
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
    
    def calcular_primer_total(e):
        try:
            cantidad = float(cantidad_tf.value)
            precio = float(precio_tf.value)
            total = cantidad * precio
            total_tf.value = f"{total:.2f}"
            total_tf.update()
        except ValueError:
            pass  # Ignora mientras se escribe un número inválido
    # Asignar la función a los eventos on_change
    cantidad_tf.on_change = calcular_primer_total
    precio_tf.on_change = calcular_primer_total
    
    def actualizar_total(e):
        fila = e.control.data  # fila = (cantidad_field, iva_field, total_text)
        try:
            cantidad = float(fila[0].value)
            precio = float(fila[1].value)
            total =  cantidad * precio
            fila[2].value = f"{total:.2f}"
            fila[2].update()
        except ValueError:
            fila[2].value = "Error"
            fila[2].update()
            
    def recalcular_totales():
        subtotal = 0.0
        iva = 0.0

        for fila in tabla_oc.rows:
            try:
                checkbox_cell = fila.cells[6].content  # Checkbox en columna 0 (ajusta si es otra)
                total_cell = fila.cells[5].content     # Total en columna 6 (índice 5)

                if isinstance(total_cell, ft.Text):
                    valor = float(total_cell.value or 0)
                    subtotal += valor

                    # Si checkbox NO está seleccionado, suma IVA para esta fila
                    if hasattr(checkbox_cell, 'value') and not checkbox_cell.value:
                        iva += valor * 0.15

            except Exception as e:
                print("Error al calcular total:", e)

        total = subtotal + iva

        sub_total_oc.value = f"{subtotal:.2f}"
        iva_oc.value = f"{iva:.2f}"
        total_oc.value = f"{total:.2f}"

        sub_total_oc.update()
        iva_oc.update()
        total_oc.update()
        
    def actualizar_total_desde_fila(e):
        for fila in tabla_oc.rows:
            cantidad_cell = fila.cells[3].content  # TextField cantidad
            precio_cell = fila.cells[4].content    # TextField precio
            total_cell = fila.cells[5].content     # Text total

            if e.control == cantidad_cell or e.control == precio_cell:
                try:
                    cantidad = float(cantidad_cell.value or 0)
                    precio = float(precio_cell.value or 0)
                    total = cantidad * precio
                    total_cell.value = f"{total:.2f}"
                except Exception as ex:
                    total_cell.value = "0.00"
                    print("Error al actualizar total de fila:", ex)

                total_cell.update()
                break

        recalcular_totales()
                
    def agregar_fila_tabla_oc(e):
        
        fila_id = len(tabla_oc.rows) + 1
        checkbox = ft.Checkbox(value=checkbox_1.value,data=fila_id, on_change=checkbox_changed)
        
        cantidad_field = ft.TextField(value=cantidad_tf.value, width=80)
        precio_field = ft.TextField(value=precio_tf.value, width=80)
        total_field = ft.Text(value=total_tf.value, width=80)

        # Asignar la lógica de actualización automática
        cantidad_field.data = (cantidad_field, precio_field, total_field)
        precio_field.data = (cantidad_field, precio_field, total_field)

        cantidad_field.on_change = actualizar_total_desde_fila
        precio_field.on_change = actualizar_total_desde_fila

        # Crear la fila (se crea primero para luego asignarla como data)
        fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(codigo_tf.value)),
                ft.DataCell(ft.Text(descripcion_tf.value)),
                ft.DataCell(ft.Text(unidad_tf.value)),
                ft.DataCell(cantidad_field),
                ft.DataCell(precio_field),
                ft.DataCell(total_field),
                ft.DataCell(checkbox),
                ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", data=None, on_click=eliminar_fila_oc)),  # Placeholder
            ]
        )

        # Asignar la propia fila como `data` del botón eliminar
        fila.cells[-1].content.data = fila  # El botón está en la última celda

        tabla_oc.rows.append(fila)
        recalcular_totales()
        
        tabla_oc.update()

        # Limpiar campos
        codigo_tf.value = ""
        descripcion_tf.value = ""
        unidad_tf.value = ""
        cantidad_tf.value = ""
        precio_tf.value = ""
        total_tf.value = ""
        checkbox_1.value = False
        checkbox_1.update()
        codigo_tf.update()
        descripcion_tf.update()
        unidad_tf.update()
        cantidad_tf.update()
        precio_tf.update()
        total_tf.update()
    
    def eliminar_fila_oc(e):
        fila_a_eliminar = e.control.data  # Data es el objeto DataRow a eliminar
        if fila_a_eliminar in tabla_oc.rows:
            tabla_oc.rows.remove(fila_a_eliminar)
            recalcular_totales()
            tabla_oc.update()
        
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

    def on_guardar_oc(e):
        datos = [(codigo, tf.value) for codigo, tf in productos_cantidad_fields]
        print("Datos capturados (código, cantidad):", datos)
        # Aquí puedes hacer algo con esos datos, por ejemplo filtrarlos:
        datos_validos = [(c, q) for c, q in datos if q.strip() != ""]
        print("Solo datos válidos:", datos_validos)
        
    def imprimir_tabla_oc(e):
        generar_pdf(tabla_oc, proveedor_tf, ruc_tf, fecha_oc,sub_total_oc, iva_oc, total_oc)

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


    # TAB Orden de compra
    tab_orden_compra = ft.Container(
        padding=10,
        expand=True,
        content=ft.Column(
            expand= True,
            controls=[
                ft.Container(
                    height=150,
                    alignment=ft.alignment.center_left,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    # Columna 1: TextFields y botones
                                    ft.Column(
                                        controls=[
                                            ft.Row([ft.Text(
                                        "Fecha:",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE
                                    ),fecha_oc,
                                                    ft.ElevatedButton(
                                                    "Elegir fecha",
                                                    width=150,
                                                    height=50,
                                                    color=ft.Colors.WHITE,
                                                    icon=ft.Icons.CALENDAR_MONTH,
                                                    bgcolor= ft.Colors.YELLOW_700,
                                                    on_click=open_date_picker,
                                                    style=ft.ButtonStyle(
                                                        padding=10,
                                                        shape=ft.RoundedRectangleBorder(radius=8),
                                                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                                                    )
                                                ),
                                                    moneda_oc
                                                    ]),
                                            ft.Row([codigo_tf, descripcion_tf, unidad_tf, cantidad_tf, precio_tf, total_tf,checkbox_1]),
                                            ft.Row([
                                                ruc_tf, proveedor_tf,
                                                ft.ElevatedButton(
                                                    "Agregar a OC",
                                                    width=150,
                                                    height=50,
                                                    on_click=agregar_fila_tabla_oc,
                                                    icon=ft.Icons.ADD,
                                                    bgcolor=ft.Colors.ORANGE,
                                                    color=ft.Colors.WHITE,
                                                    style=ft.ButtonStyle(
                                                        padding=10,
                                                        shape=ft.RoundedRectangleBorder(radius=8),
                                                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                                                    )
                                                ),
                                                ft.ElevatedButton(
                                                    "Guardar OC",
                                                    width=150,
                                                    height=50,
                                                    on_click=agregar_fila_tabla_oc,
                                                    icon=ft.Icons.SAVE,
                                                    bgcolor=ft.Colors.GREEN,
                                                    color=ft.Colors.WHITE,
                                                    style=ft.ButtonStyle(
                                                        padding=10,
                                                        shape=ft.RoundedRectangleBorder(radius=8),
                                                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                                                    )
                                                ),
                                                ft.ElevatedButton(
                                                    "Imprimir",
                                                    width=150,
                                                    height=50,
                                                    on_click=imprimir_tabla_oc,
                                                    icon=ft.Icons.PRINT_ROUNDED,
                                                    bgcolor=ft.Colors.BLUE_ACCENT,
                                                    color=ft.Colors.WHITE,
                                                    style=ft.ButtonStyle(
                                                        padding=10,
                                                        shape=ft.RoundedRectangleBorder(radius=8),
                                                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                                                    )
                                                )
                                            ])
                                        ],
                                        expand=True
                                    ),

                                    # Columna 2: Totales
                                    ft.Column(
                                        controls=[
                                            ft.Text("SubTotal:", weight=ft.FontWeight.BOLD),
                                            sub_total_oc,
                                            ft.Text("IVA:", weight=ft.FontWeight.BOLD),
                                            iva_oc,
                                            ft.Text("TOTAL:", weight=ft.FontWeight.BOLD),
                                            total_oc
                                        ],
                                        alignment=ft.MainAxisAlignment.START
                                    )
                                ]
                            ),
                        ]
                    )
                ),

                ft.Container(
                    padding=ft.padding.symmetric(vertical=20),
                    content=ft.Row(
                        alignment=ft.alignment.center_left,
                        spacing=10,
                        controls=[
                            ft.Icon(name=ft.Icons.INVENTORY_2, color=ft.Colors.GREY_700),
                            ft.Text("Productos agregados a la orden", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                        ]
                    )
                ),
                ft.Divider(thickness=2, color=ft.Colors.GREY_400),
                tabla_oc
            ],
            scroll="auto"
        )
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
        content=tab_orden_compra  # Directamente las tabs sin Rows ni Columns extras
    )
       
    # Devolver el contenedor y el evento de carga inicial
    return {
        "container": contenedor,
        "dropdown_event": lambda e=None: on_categoria_change(e)
    }
