import flet as ft

def main(page: ft.Page):
    page.title = "Galería de Iconos Inventario y Productos"
    page.scroll = "auto"

    iconos = [
        ("INVENTORY", ft.Icons.INVENTORY),
        ("INVENTORY_2", ft.Icons.INVENTORY_2),
        ("WAREHOUSE", ft.Icons.WAREHOUSE),
        ("STORE", ft.Icons.STORE),
        ("STOREFRONT", ft.Icons.STOREFRONT),
        ("SHOPPING_CART", ft.Icons.SHOPPING_CART),
        ("SHOPPING_BAG", ft.Icons.SHOPPING_BAG),
        ("LOCAL_GROCERY_STORE", ft.Icons.LOCAL_GROCERY_STORE),
        ("CHECKLIST", ft.Icons.CHECKLIST),
        ("FACT_CHECK", ft.Icons.FACT_CHECK),
        ("DESCRIPTION", ft.Icons.DESCRIPTION),
        ("RECEIPT", ft.Icons.RECEIPT),
        ("RECEIPT_LONG", ft.Icons.RECEIPT_LONG),
        ("CATEGORY", ft.Icons.CATEGORY),
        ("FACTORY", ft.Icons.FACTORY),
        ("CREDIT_CARD", ft.Icons.CREDIT_CARD),
        ("ATTACH_MONEY", ft.Icons.ATTACH_MONEY),
        ("MONETIZATION_ON", ft.Icons.MONETIZATION_ON),
        ("LOCAL_SHIPPING", ft.Icons.LOCAL_SHIPPING),
        ("DELIVERY_DINING", ft.Icons.DELIVERY_DINING),
        ("ASSESSMENT", ft.Icons.ASSESSMENT),
        ("PRECISION_MANUFACTURING", ft.Icons.PRECISION_MANUFACTURING),
        ("BUILD", ft.Icons.BUILD),
        ("SETTINGS", ft.Icons.SETTINGS),
        ("INTEGRATION_INSTRUCTIONS", ft.Icons.INTEGRATION_INSTRUCTIONS),

        # Documentos / Listados
        ("ARTICLE", ft.Icons.ARTICLE),
        ("FILE_PRESENT", ft.Icons.FILE_PRESENT),
        ("LIST_ALT", ft.Icons.LIST_ALT),
        ("NOTE_ADD", ft.Icons.NOTE_ADD),
        ("SOURCE", ft.Icons.SOURCE),

        # Pagos / Finanzas
        ("ACCOUNT_BALANCE", ft.Icons.ACCOUNT_BALANCE),
        ("PAYMENT", ft.Icons.PAYMENT),
        ("ATTACH_MONEY", ft.Icons.ATTACH_MONEY),
        ("RECEIPT", ft.Icons.RECEIPT),

        # Envíos / Transporte
        ("LOCAL_POST_OFFICE", ft.Icons.LOCAL_POST_OFFICE),
        ("MOVING", ft.Icons.MOVING),
        ("LOCAL_TAXI", ft.Icons.LOCAL_TAXI),
        
        ("PEOPLE", ft.Icons.PEOPLE),                      # Personas / contactos
        ("GROUP", ft.Icons.GROUP),                        # Grupo de personas
        ("HANDSHAKE", ft.Icons.HANDSHAKE),                # Acuerdo / contrato (Material Icons no lo tiene, alternativa: use SUPPORT_AGENT)
        ("SUPPORT_AGENT", ft.Icons.SUPPORT_AGENT),        # Soporte / atención
        ("BUSINESS", ft.Icons.BUSINESS),                   # Empresa / negocio
        ("STORE", ft.Icons.STORE),                         # Tienda / local
        ("LOCAL_SHIPPING", ft.Icons.LOCAL_SHIPPING),       # Envío / logística
        ("CONTACT_MAIL", ft.Icons.CONTACT_MAIL),           # Contacto por email
        ("PHONE", ft.Icons.PHONE),                         # Teléfono
        ("MAIL", ft.Icons.MAIL),                           # Correo
        ("APARTMENT", ft.Icons.APARTMENT),                 # Oficina / edificio
        ("WORK", ft.Icons.WORK),                           # Trabajo / profesional
        
        ("PEOPLE", ft.Icons.PEOPLE),                       # Personas
        ("GROUP", ft.Icons.GROUP),                         # Grupo de personas
        ("PERSON", ft.Icons.PERSON),                       # Persona individual
        ("PERSON_ADD", ft.Icons.PERSON_ADD),               # Añadir persona
        ("WORK", ft.Icons.WORK),                           # Trabajo / empleo
        ("BADGE", ft.Icons.BADGE),                         # Identificación
        ("ASSIGNMENT", ft.Icons.ASSIGNMENT),               # Asignación / tareas
        ("ASSIGNMENT_IND", ft.Icons.ASSIGNMENT_IND),       # Asignación individual
        ("SUPPORT_AGENT", ft.Icons.SUPPORT_AGENT),         # Soporte / HR
        ("ACCESSIBILITY", ft.Icons.ACCESSIBILITY),         # Accesibilidad
        ("SCHOOL", ft.Icons.SCHOOL),                       # Formación / capacitación
        ("CONTACT_PHONE", ft.Icons.CONTACT_PHONE),         # Contacto telefónico
        ("EMAIL", ft.Icons.EMAIL),                         # Correo electrónico
        ("EVENT", ft.Icons.EVENT),                         # Eventos / reuniones
        ("WORK_HISTORY", ft.Icons.WORK_HISTORY),           # Historial laboral
        ("ACCOUNT_BOX", ft.Icons.ACCOUNT_BOX),             # Perfil
        
        ("ASSESSMENT", ft.Icons.ASSESSMENT),               # Evaluación / Reporte
        ("CHECK_CIRCLE", ft.Icons.CHECK_CIRCLE),           # Aprobado / Correcto
        ("HIGHLIGHT_OFF", ft.Icons.HIGHLIGHT_OFF),         # Rechazado / Incorrecto
        ("RATE_REVIEW", ft.Icons.RATE_REVIEW),             # Reseña / Evaluación
        ("GRADE", ft.Icons.GRADE),                         # Calificación
        ("TASK_ALT", ft.Icons.TASK_ALT),                   # Tarea completada
        ("FEEDBACK", ft.Icons.FEEDBACK),                   # Retroalimentación
        ("INSIGHTS", ft.Icons.INSIGHTS),                   # Análisis
        ("EVENT_NOTE", ft.Icons.EVENT_NOTE),               # Nota de evento
        ("REPORT", ft.Icons.REPORT),                        # Reporte
        ("DONE", ft.Icons.DONE),                            # Listo / Hecho
    ]

    grid = ft.GridView(
        expand=1,
        runs_count=4,
        max_extent=150,
        child_aspect_ratio=1,
        spacing=10,
        run_spacing=10,
    )

    for nombre, icono in iconos:
        grid.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(icono, size=40, color=ft.Colors.BLUE_700),
                        ft.Text(nombre, size=12, text_align="center"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=10,
                bgcolor=ft.Colors.GREY_100,
                border_radius=8,
            )
        )

    page.add(grid)

ft.app(target=main)
