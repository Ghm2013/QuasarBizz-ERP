from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
import datetime
import os
import platform
import subprocess  # Para abrir el archivo PDF

def generar_pdf(tabla_oc, proveedor_ctrl, ruc_ctrl, fecha_ctrl, sub_total_oc, iva_oc, total_oc):
    ruta_archivo = "orden_compra.pdf"
    c = canvas.Canvas(ruta_archivo, pagesize=A4)
    width, height = A4

    # --- Encabezado: Título y logo ---
    logo_path = "assets/QuasarBizz ERP.jpg"  # Ruta al logo (ajústala)
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 40, height - 100, width=80, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, height - 60, "Orden de Compra")

    # --- Datos del proveedor ---
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 130, f"Proveedor: {proveedor_ctrl.value}")
    c.drawString(300, height - 130, f"RUC: {ruc_ctrl.value}")
    c.drawString(40, height - 150, f"Fecha: {fecha_ctrl.value or datetime.date.today().strftime('%d/%m/%Y')}")

    # --- Tabla con los productos ---
    data = [["#", "Descripción", "Unidad", "Cantidad", "Precio", "Total"]]
    for idx, fila in enumerate(tabla_oc.rows, start=1):
        desc = fila.cells[1].content.value
        unidad = fila.cells[2].content.value
        cantidad = fila.cells[3].content.value
        precio = fila.cells[4].content.value
        total = fila.cells[5].content.value
        data.append([str(idx), desc, unidad, cantidad, precio, total])

    table = Table(data, colWidths=[30, 180, 60, 60, 60, 60])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))

    # Posicionamos la tabla
    table.wrapOn(c, width, height)
    table.drawOn(c, 40, height - 200 - 20 * len(data))

    # --- Totales ---
    y_pos = height - 200 - 20 * len(data) - 40
    c.setFont("Helvetica-Bold", 11)
    c.drawString(350, y_pos, f"Subtotal: {sub_total_oc.value}")
    c.drawString(350, y_pos - 15, f"IVA: {iva_oc.value}")
    c.drawString(350, y_pos - 30, f"Total: {total_oc.value}")

    c.save()
    print(f"PDF generado: {ruta_archivo}")

    # --- Abrir automáticamente el PDF generado ---
    try:
        sistema = platform.system()
        if sistema == "Windows":
            os.startfile(ruta_archivo)
        elif sistema == "Darwin":  # macOS
            subprocess.run(["open", ruta_archivo])
        else:  # Linux o Unix
            subprocess.run(["xdg-open", ruta_archivo])
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")


def generar_consolidado_pdf(tabla, fecha):
    ruta_archivo = "Consolidado.pdf"
    c = canvas.Canvas(ruta_archivo, pagesize=A4)
    width, height = A4

    # --- Encabezado: Título y logo ---
    logo_path = "assets/QuasarBizz ERP.jpg"  # Ruta al logo (ajústala)
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 40, height - 100, width=80, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, height - 60, "Solicitud Mensual")

    # --- Datos del proveedor ---
    """c.setFont("Helvetica", 11)
    c.drawString(40, height - 130, f"Proveedor: {proveedor_ctrl.value}")
    c.drawString(300, height - 130, f"RUC: {ruc_ctrl.value}")"""
    c.drawString(40, height - 150, f"Fecha: {fecha.value or datetime.date.today().strftime('%d/%m/%Y')}")

    # --- Tabla con los productos ---
    data = [["#", "Descripción", "Unidad", "Cantidad", "Precio", "Total"]]
    for idx, fila in enumerate(tabla.rows, start=1):
        desc = fila.cells[1].content.value
        unidad = fila.cells[2].content.value
        cantidad = fila.cells[3].content.value
        precio = fila.cells[4].content.value
        total = fila.cells[5].content.value
        data.append([str(idx), desc, unidad, cantidad, precio, total])

    table = Table(data, colWidths=[30, 180, 60, 60, 60, 60])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))

    # Posicionamos la tabla
    table.wrapOn(c, width, height)
    table.drawOn(c, 40, height - 200 - 20 * len(data))

    # --- Totales ---
    """y_pos = height - 200 - 20 * len(data) - 40
    c.setFont("Helvetica-Bold", 11)
    c.drawString(350, y_pos, f"Subtotal: {sub_total_oc.value}")
    c.drawString(350, y_pos - 15, f"IVA: {iva_oc.value}")
    c.drawString(350, y_pos - 30, f"Total: {total_oc.value}")"""

    c.save()
    print(f"PDF generado: {ruta_archivo}")

    # --- Abrir automáticamente el PDF generado ---
    try:
        sistema = platform.system()
        if sistema == "Windows":
            os.startfile(ruta_archivo)
        elif sistema == "Darwin":  # macOS
            subprocess.run(["open", ruta_archivo])
        else:  # Linux o Unix
            subprocess.run(["xdg-open", ruta_archivo])
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")