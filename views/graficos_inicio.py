import flet as ft
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd

# ============================
# DATOS SIMULADOS PARA 2 AÑOS
# ============================
df_cumplimiento = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"] * 2,
    "Año": [2023] * 12 + [2024] * 12,
    "Cumplimiento": [
        70, 65, 80, 75, 90, 85, 60, 78, 88, 82, 79, 91,     # 2023
        75, 70, 85, 80, 88, 90, 65, 82, 92, 87, 84, 95      # 2024
    ]
})


def generar_grafico(meses: list, año1: int, año2: int = None) -> str:
    df1 = df_cumplimiento[(df_cumplimiento["Año"] == año1) & (df_cumplimiento["Mes"].isin(meses))]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(meses))
    width = 0.35

    if año2 and año2 != año1:
        df2 = df_cumplimiento[(df_cumplimiento["Año"] == año2) & (df_cumplimiento["Mes"].isin(meses))]
        ax.bar([i - width/2 for i in x], df1["Cumplimiento"], width=width, label=str(año1), color="#4CAF50")
        ax.bar([i + width/2 for i in x], df2["Cumplimiento"], width=width, label=str(año2), color="#2196F3")

        # Etiquetas encima de las barras
        for i, val in enumerate(df1["Cumplimiento"]):
            ax.text(i - width/2, val + 1, f"{val}%", ha='center', fontsize=8)
        for i, val in enumerate(df2["Cumplimiento"]):
            ax.text(i + width/2, val + 1, f"{val}%", ha='center', fontsize=8)
        titulo = f"Comparativo de Cumplimiento: {año1} vs {año2}"
    else:
        ax.bar(x, df1["Cumplimiento"], width=width, color="#4CAF50", label=str(año1))
        for i, val in enumerate(df1["Cumplimiento"]):
            ax.text(i, val + 1, f"{val}%", ha='center', fontsize=9)
        titulo = f"Cumplimiento mensual en {año1}"

    ax.set_xticks(x)
    ax.set_xticklabels(meses)
    ax.set_ylim(0, 110)
    ax.set_ylabel("Cumplimiento (%)")
    ax.set_title(titulo)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


def main(page: ft.Page):
    page.title = "Cumplimiento por Año (Comparativo Opcional)"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    años = sorted(df_cumplimiento["Año"].unique())

    # Dropdowns
    dd_anio1 = ft.Dropdown(
        label="Año base",
        options=[ft.dropdown.Option(str(a)) for a in años],
        value=str(años[0]),
        width=120
    )

    dd_anio2 = ft.Dropdown(
        label="Año a comparar (opcional)",
        options=[ft.dropdown.Option(str(a)) for a in años],
        value=str(años[1]),
        width=180
    )

    dd_inicio = ft.Dropdown(
        label="Mes de inicio",
        options=[ft.dropdown.Option(m) for m in meses],
        value="Ene",
        width=150
    )

    dd_fin = ft.Dropdown(
        label="Mes de fin",
        options=[ft.dropdown.Option(m) for m in meses],
        value="Dic",
        width=150
    )

    mensaje = ft.Text("Puedes seleccionar un solo año o comparar dos años.")
    img = ft.Image(width=800, height=400, visible=True)

    # Mostrar gráfico inicial con todo el año
    grafico_inicial = generar_grafico(meses, años[0], años[1])
    img.src_base64 = grafico_inicial

    def actualizar(e):
        try:
            i_ini = meses.index(dd_inicio.value)
            i_fin = meses.index(dd_fin.value)
            año1 = int(dd_anio1.value)
            año2 = int(dd_anio2.value)

            if i_ini > i_fin:
                mensaje.value = "⚠️ El mes de inicio debe ser anterior o igual al de fin."
                img.visible = False
            else:
                rango_meses = meses[i_ini:i_fin + 1]
                img.src_base64 = generar_grafico(rango_meses, año1, año2)
                if año1 == año2:
                    mensaje.value = f"Mostrando cumplimiento de {año1} ✅"
                else:
                    mensaje.value = f"Comparando {año1} vs {año2} de {dd_inicio.value} a {dd_fin.value} ✅"
                img.visible = True
            page.update()
        except Exception as ex:
            mensaje.value = f"❌ Error: {ex}"
            img.visible = False
            page.update()

    boton = ft.ElevatedButton(text="Mostrar gráfico", on_click=actualizar)

    page.add(
        ft.Row([dd_anio1, dd_anio2], spacing=20),
        ft.Row([dd_inicio, dd_fin, boton], spacing=20),
        img,
        mensaje
    )


ft.app(target=main)
