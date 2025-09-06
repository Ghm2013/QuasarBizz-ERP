# archivo: views.py
import flet as ft
from database import get_data, insert_data, get_connection

def build_table(data, nombre_tabla, tabla_widget):
    def make_on_submit(row_id):
        def handler(e):
            nuevo_valor = e.control.value.strip()
            if nuevo_valor:
                campo = "nombre" if nombre_tabla == "clientes" else "descripcion"
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(f"UPDATE {nombre_tabla} SET {campo} = ? WHERE id = ?", (nuevo_valor, row_id))
                conn.commit()
                conn.close()
                # Refrescar tabla
                nueva_data = get_data(nombre_tabla)
                tabla_widget.controls[0] = build_table(nueva_data, nombre_tabla, tabla_widget)
                tabla_widget.update()
        return handler

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Valor (editable)")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(row[0]))),
                    ft.DataCell(
                        ft.TextField(
                            value=row[1],
                            on_submit=make_on_submit(row[0]),
                            border_color=ft.colors.TRANSPARENT,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            dense=True,
                        )
                    )
                ]
            )
            for row in data
        ] if data else []
    )

def crear_tab(nombre_tabla, campo_label):
    data = get_data(nombre_tabla)
    tabla_widget = ft.Column([])

    entrada = ft.TextField(label=campo_label, expand=True)
    boton_agregar = ft.ElevatedButton(text="Agregar")

    def agregar_click(e):
        if entrada.value.strip():
            insert_data(nombre_tabla, entrada.value)
            nueva_data = get_data(nombre_tabla)
            tabla_widget.controls = [build_table(nueva_data, nombre_tabla, tabla_widget)]
            tabla_widget.update()
            entrada.value = ""
            entrada.update()

    boton_agregar.on_click = agregar_click

    tabla_widget.controls.append(build_table(data, nombre_tabla, tabla_widget))

    return ft.Tab(
        text=nombre_tabla.capitalize(),
        content=ft.Column([
            ft.Row([entrada, boton_agregar]),
            tabla_widget
        ])
    )
