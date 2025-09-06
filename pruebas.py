# archivo: views.py
import flet as ft
import pandas as pd
from database import get_connection

excel_df = None  # Variable global temporal para almacenar el DataFrame

def cargar_excel_desde_archivo(e, tabla_widget):
    global excel_df
    if e.files:
        archivo = e.files[0].path
        excel_df = pd.read_excel(archivo)

        # Mostrar en tabla
        tabla_widget.controls.clear()
        tabla_widget.controls.append(
            ft.DataTable(
                columns=[ft.DataColumn(ft.Text(col)) for col in excel_df.columns],
                rows=[
                    ft.DataRow([
                        ft.DataCell(ft.Text(str(value))) for value in fila
                    ]) for fila in excel_df.itertuples(index=False)
                ]
            )
        )
        tabla_widget.update()

def guardar_en_bd_click(e):
    global excel_df
    if excel_df is not None:
        conn = get_connection()
        cursor = conn.cursor()

        for _, fila in excel_df.iterrows():
            cursor.execute("""
                INSERT INTO Productos (Codigo, nombre, Unidad_de_medida, categoria)
                VALUES (?, ?, ?, ?);
            """, (
                fila['Codigo'],
                fila['Nombre'],
                fila['Unidad de medida'],
                int(fila['Categoria'])
            ))

        conn.commit()
        conn.close()
        print("Datos guardados en SQLite Cloud correctamente.")

def main(page: ft.Page):
    page.title = "Importar Excel"
    tabla_widget = ft.Column()

    file_picker = ft.FilePicker(on_result=lambda e: cargar_excel_desde_archivo(e, tabla_widget))
    page.overlay.append(file_picker)  # Necesario para que funcione el FilePicker

    boton_archivo = ft.ElevatedButton("Seleccionar archivo Excel", on_click=lambda e: file_picker.pick_files(allow_multiple=False))
    boton_guardar = ft.ElevatedButton("Guardar en base de datos", on_click=guardar_en_bd_click)

    page.add(
        ft.Column([
            boton_archivo,
            boton_guardar,
            tabla_widget
        ])
    )

ft.app(target=main)
