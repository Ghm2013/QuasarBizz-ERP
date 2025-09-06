import threading
import flet as ft
import sys
import os

from consultas import cerrar_sesion
from views import oc
from views.consolidado_compra import crear_formulario_consol_solicitud
from views.solicitud_compra_mensual import crear_formulario_sol_compra
from views.cargarproductos import crear_formulario_cargar_excel
from views.newuser import crear_formulario_newuser

# --- Función para obtener la ruta de los recursos ---
def resource_path(relative_path):
    """Obtiene la ruta absoluta a los recursos, ya sea desde el entorno de desarrollo o desde el paquete de PyInstaller."""
    try:
        base_path = sys._MEIPASS # Ruta temporal de PyInstaller
    except Exception:
        base_path = os.path.abspath(".") # Ruta del directorio actual en modo de desarrollo
    
    return os.path.join(base_path, relative_path)


# Valores de usuario de ejemplo para correr el código
#usuario_actual = sys.argv[1] if len(sys.argv) > 1 else "Invitado"
#correo_actual = sys.argv[2] if len(sys.argv) > 1 else "invitado@quassar.com"

# --- Estructura de datos para definir el menú y los formularios ---
MENU_CONFIG = {
    "recursos_humanos": {
        "icono": ft.Icons.PEOPLE_ALT_SHARP,
        "tooltip": "Recursos Humanos",
        "texto": "Recursos Humanos",
        "submenu": [
            {"texto": "Empleados", "icono": ft.Icons.PERSON, "formulario": ft.Text("Formulario de Empleados", size=20)},
            {"texto": "Solicitar Vacante", "icono": ft.Icons.BADGE, "formulario": ft.Text("Nueva Vacante", size=20)},
            {"texto": "Nómina", "icono": ft.Icons.MONETIZATION_ON, "formulario": ft.Text("Formulario de Nómina", size=20)},
            {"texto": "Contratación", "icono": ft.Icons.GROUP_ADD, "formulario": ft.Text("Formulario de Contratación", size=20)}
        ]
    },
    "inventario": {
        "icono": ft.Icons.INVENTORY,
        "tooltip": "Inventario",
        "texto": "Inventario",
        "submenu":[
            {"texto": "Agregar Productos", "icono": ft.Icons.BALLOT, "formulario": ft.Text("Formulario de Producto", size=20)},
            {"texto": "Carga por Lotes de Productos", "icono": ft.Icons.WAREHOUSE, "formulario": crear_formulario_cargar_excel},
            {"texto": "Modificar Producto", "icono": ft.Icons.DESCRIPTION, "formulario": ft.Text("Modificar Producto", size=20)},
            {"texto": "Agregar Categoría", "icono": ft.Icons.CATEGORY, "formulario": ft.Text("Categoria de Productos", size=20)}
                ]
            },
    "Proveedores": {
        "icono": ft.Icons.LOCAL_SHIPPING,
        "tooltip": "Proveedores",
        "texto": "Proveedores",
        "submenu":[
            {"texto": "Agregar Proveedor", "icono": ft.Icons.PERSON_ADD, "formulario": ft.Text("Formulario de Proveedores", size=20)},
            {"texto": "Evaluaciones de proveedores", "icono": ft.Icons.FACT_CHECK, "formulario": ft.Text("Formulario Evaluacion de proveedores", size=20)},
            {"texto": "Contratación", "icono": ft.Icons.GROUP_ADD, "formulario": ft.Text("Formulario de Contratación", size=20)}
                ]
            },

    "presupuesto": {
        "icono": ft.Icons.ACCOUNT_BALANCE_WALLET,
        "tooltip": "Presupuesto",
        "texto": "Presupuesto",
        "submenu": [
            {"texto": "Agregar presupuesto", "icono": ft.Icons.ACCOUNT_BALANCE, "formulario": ft.Text("Formulario agregar presupuesto", size=20)},
            {"texto": "Modificar Presupuesto", "icono": ft.Icons.RECEIPT, "formulario": ft.Text("Modificar Presupuesto", size=20)},
            {"texto": "Ejecución de Presupuesto", "icono": ft.Icons.PAYMENT, "formulario": ft.Text("Formulario Ejecución de Presupuesto", size=20)}
        ]
    },
    "compras": {
        "icono": ft.Icons.STORE,
        "tooltip": "Compras",
        "texto": "Compras",
        "submenu": [
            {"texto": "Solicitud Compra", "icono": ft.Icons.SHOPPING_BAG,  "formulario": ft.Text("Formulario de Entrada de Producto", size=20)},
            {"texto": "Solicitud Compra Mensual", "icono": ft.Icons.ADD_SHOPPING_CART, "formulario": crear_formulario_sol_compra},
            {"texto": "Consolidado Solicitud Mensual", "icono": ft.Icons.VIEW_AGENDA, "formulario": crear_formulario_consol_solicitud},
            {"texto": "Orden de Compra", "icono": ft.Icons.RECEIPT_LONG, "formulario": oc.crear_formulario_oc},
            {"texto": "Listado de Órdenes de Compra", "icono": ft.Icons.TABLE_ROWS, "formulario": ft.Text("Formulario de Órdenes de Compra", size=20)},
            {"texto": "Solicitud de Pago", "icono": ft.Icons.ATTACH_MONEY, "formulario": ft.Text("Formulario de Solciitud de Pago", size=20)},
            {"texto": "Listado de Solicitudes de Pago", "icono": ft.Icons.ARTICLE, "formulario": ft.Text("Formulario de Solicitudes de PAgo", size=20)}
        ]
    },
    "configuracion": {
        "icono": ft.Icons.SETTINGS,
        "tooltip": "Configuración",
        "texto": "Configuración",
        "formulario": ft.Text("Configuración del sistema", size=20)
    },
    "perfil": {
        "icono": ft.Icons.PERSON,
        "tooltip": "Perfil",
        "texto": "Perfil",
        "submenu": [ 
            { "texto": "Nuevo Usuario", "icono": ft.Icons.PERSON_ADD, "formulario": crear_formulario_newuser },
         ]
    }
}

def main_app(page: ft.Page, usuario_id, usuario_actual, correo_actual):
    page.title = "QuasarBizz ERP"
    page.window.icon = resource_path("assets/iconos/QZERP_ico.ico")
    page.window.maximized = True
    page.window.resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    pestañas_abiertas = {}

    contenido_principal_tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[],
    )

    submenu_container = ft.Container(
        width=200,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE),
        border_radius=ft.border_radius.all(10),
        padding=ft.padding.all(10),
        visible=False,
    )
    def cerrar_ventana_segura():
        page.window.prevent_close = False
        page.window.on_event = None
        page.window.close()

        
    def close_session(e):
        
        resultado = cerrar_sesion(correo_actual)
        
        if resultado[1] == 0:
# Importar login aquí dentro, no al inicio
            import login
            async def volver_login():
                page.clean()
                page.appbar = None  # Quita la AppBar
                page.floating_action_button = None 
                await login.login_main(page)
            page.run_task(volver_login)
        else:
            print("Error al cerrar la sesión.")
    
    def on_window_event(e):
        if e.data == "close":
            t = threading.Thread(target=lambda: close_session(e))
            t.start() 
            
    page.window.on_event = on_window_event
    page.window.prevent_close = True 
    
    def cerrar_tab(e):
        opcion_a_cerrar = e.control.data
        if opcion_a_cerrar in pestañas_abiertas:
            tab_a_eliminar = pestañas_abiertas[opcion_a_cerrar]
            contenido_principal_tabs.tabs.remove(tab_a_eliminar)
            del pestañas_abiertas[opcion_a_cerrar]
            if not contenido_principal_tabs.tabs:
                 submenu_container.visible = False
            page.update()

    def manejar_tab(opcion_id, titulo_tab, formulario_objeto):
        if opcion_id in pestañas_abiertas:
            contenido_principal_tabs.selected_index = contenido_principal_tabs.tabs.index(pestañas_abiertas[opcion_id])
        else:
            contenido_tab = None
            dropdown_event = None
            if callable(formulario_objeto):
                form_result = formulario_objeto(page)
                if isinstance(form_result, dict):
                    contenido_tab = form_result["container"]
                    dropdown_event = form_result.get("dropdown_event")
                else:
                    contenido_tab = form_result
            else:
                contenido_tab = formulario_objeto

            nueva_tab = ft.Tab(
                text=titulo_tab,
                content=contenido_tab,
                tab_content=ft.Row(
                    controls=[
                        ft.Text(titulo_tab, color=ft.Colors.WHITE),
                        ft.IconButton(
                            ft.Icons.CLOSE,
                            icon_size=15,
                            data=opcion_id,
                            on_click=cerrar_tab
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
            contenido_principal_tabs.tabs.append(nueva_tab)
            pestañas_abiertas[opcion_id] = nueva_tab
            contenido_principal_tabs.selected_index = len(contenido_principal_tabs.tabs) - 1
            
            page.update() # Se actualiza la página aquí para que el contenedor esté presente
            if dropdown_event:
                dropdown_event() # Y ahora se llama el evento de inicialización del dropdown
        
        submenu_container.visible = False
        page.update()

    def cargar_opcion_final_submenu(e, opcion_submenu):
        manejar_tab(opcion_submenu["texto"], opcion_submenu["texto"], opcion_submenu["formulario"])

    def cargar_formulario(e, opcion_id):
        opcion_config = MENU_CONFIG[opcion_id]
        if "submenu" in opcion_config:
            submenu_content = ft.Column(
                controls=[
                    ft.Text(
                        opcion_config["texto"],
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(),
                    ft.Column(
                        controls=[
                            ft.ListTile(
                                title=ft.Text(item["texto"],color = ft.Colors.WHITE, size= 12),
                                leading=ft.Icon(item["icono"],color = ft.Colors.WHITE,),
                                on_click=lambda e, item=item: cargar_opcion_final_submenu(e, item)
                            ) for item in opcion_config["submenu"]
                        ],
                        spacing=0
                    )
                ]
            )
            submenu_container.content = submenu_content
            submenu_container.visible = True
        else:
            manejar_tab(opcion_id, opcion_config["texto"], opcion_config["formulario"])
        page.update()
    menu_lateral = ft.Container(
        width=50,
        bgcolor=ft.Colors.PURPLE_900,
        content=ft.Column(
            controls=[
                *[ft.IconButton(
                    MENU_CONFIG[opcion]["icono"],
                    tooltip=MENU_CONFIG[opcion]["tooltip"],
                    icon_color=ft.Colors.WHITE70,
                    on_click=lambda e, opt=opcion: cargar_formulario(e, opt)
                ) for opcion in MENU_CONFIG]
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.appbar = ft.AppBar(
        leading=ft.Image(src=resource_path("assets/iconos/QuasarBizz_ERP-amplio.png"), width=200, height=42),
        title=ft.Text("QuasarBizz ERP v1.0", size=18, weight=ft.FontWeight.BOLD, color= ft.Colors.PURPLE_50), 
        center_title=False,
        bgcolor=ft.Colors.BLACK87,
        actions=[
            ft.Text(f"Usuario: ", color=ft.Colors.BLUE_700, size=14, weight=ft.FontWeight.BOLD),
            ft.Text(f"{usuario_actual}", color=ft.Colors.WHITE, size=14),
            ft.Container(width=20),
            ft.Text(f"Correo: ", color=ft.Colors.BLUE_700, size=14, weight=ft.FontWeight.BOLD),
            ft.Text(f"{correo_actual}", color=ft.Colors.WHITE, size=14),
            ft.Container(width=20),
            ft.IconButton(ft.Icons.LOGOUT, tooltip="Cerrar sesión", icon_color=ft.Colors.PURPLE_50, on_click=close_session)
        ],
    )
    
    def on_disconnect(e):
        cerrar_sesion(correo_actual)
        os._exit(0)

    page.on_disconnect = on_disconnect

    page.add(
        ft.Row(
            expand=True,
            controls=[
                menu_lateral,
                submenu_container,
                contenido_principal_tabs
            ]
        )
    )
