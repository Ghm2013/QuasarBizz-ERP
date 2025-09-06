import flet as ft
import pandas as pd
import os
from database import get_connection

# Variable global para almacenar el DataFrame del Excel
excel_df = None

# Contenedor de columna para la tabla
tabla_widget = ft.Column()

# Control de texto para mostrar mensajes (no un TextField)
campo_mensaje = ft.Text(
    value="",
    color=ft.Colors.YELLOW,
    weight=ft.FontWeight.BOLD
)

def cargar_excel_desde_archivo(e: ft.FilePickerResultEvent, page: ft.Page):
    global excel_df
    campo_mensaje.value = f"Cargando archivo: {os.path.basename(e.files[0].path)}..."
    campo_mensaje.color = ft.Colors.YELLOW
    campo_mensaje.update()
    
    try:
        archivo = e.files[0].path
        excel_df = pd.read_excel(archivo)
        
        # Limpiar y llenar la tabla
        tabla_widget.controls.clear()
        tabla_widget.controls.append(
            ft.DataTable(
                columns=[ft.DataColumn(ft.Text(col, color=ft.Colors.WHITE)) for col in excel_df.columns],
                rows=[
                    ft.DataRow([
                        ft.DataCell(ft.Text(str(value), color=ft.Colors.WHITE)) for value in fila
                    ]) for fila in excel_df.itertuples(index=False)
                ]
            )
        )
        
        campo_mensaje.value = "Archivo cargado y tabla actualizada correctamente."
        campo_mensaje.color = ft.Colors.GREEN
        
        tabla_widget.update()
        campo_mensaje.update()
        
    except Exception as ex:
        campo_mensaje.value = f"Error al cargar el archivo: {ex}"
        campo_mensaje.color = ft.Colors.RED
        campo_mensaje.update()
        page.update()

def guardar_en_bd_click(e, page: ft.Page):
    global excel_df
    campo_mensaje.value = ""
    campo_mensaje.update()
    
    if excel_df is not None:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            column_names = ', '.join([f'"{col}"' for col in excel_df.columns])
            placeholders = ', '.join(['?' for _ in excel_df.columns])
            sql_statement = f"INSERT INTO Productos ({column_names}) VALUES ({placeholders});"
            
            data_to_insert = [tuple(row) for row in excel_df.to_numpy()]
            
            cursor.executemany(sql_statement, data_to_insert)
            conn.commit()
            conn.close()
            
            campo_mensaje.value = "Datos guardados en la base de datos correctamente."
            campo_mensaje.color = ft.Colors.GREEN
            campo_mensaje.update()
            
        except Exception as ex:
            campo_mensaje.value = f"Error al guardar los datos: {ex}"
            campo_mensaje.color = ft.Colors.RED
            campo_mensaje.update()
    else:
        campo_mensaje.value = "No hay datos cargados para guardar."
        campo_mensaje.color = ft.Colors.ORANGE
        campo_mensaje.update()
    
    page.update()

def crear_formulario_cargar_excel(page: ft.Page):
    file_picker = ft.FilePicker(on_result=lambda e: cargar_excel_desde_archivo(e, page))
    page.overlay.append(file_picker)
    
    boton_archivo = ft.ElevatedButton(
        "Seleccionar archivo Excel",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )
    
    boton_guardar = ft.ElevatedButton(
        "Guardar en base de datos",
        icon=ft.Icons.SAVE,
        on_click=lambda e: guardar_en_bd_click(e, page)
    )

    return ft.Container(
        content=ft.Column([
            ft.Row(
                [boton_archivo, boton_guardar, campo_mensaje],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Text("Vista previa de los datos del Excel:"),
            ft.Divider(),
            ft.Row(
                controls=[tabla_widget],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE
        ),
        expand=True
    )