import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulador de Prospectiva Financiera",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Simulador de Planificación Prospectiva Financiera")
st.write("Análisis dinámico de escenarios, variables PESTEL y proyección financiera a 5 años.")

# ---------------------------------------------------------
# ESCENARIOS
# ---------------------------------------------------------

st.sidebar.header("⚙️ Configuración")

escenario = st.sidebar.selectbox(
    "Seleccione el escenario",
    ["BASE", "FAVORABLE", "ADVERSO"]
)

if escenario == "FAVORABLE":
    crecimiento_ventas = 12.0
    crecimiento_costos = 1.0
    variacion_precio = 5.0
    crecimiento_gastos = 1.0

elif escenario == "ADVERSO":
    crecimiento_ventas = -5.0
    crecimiento_costos = 8.0
    variacion_precio = 0.0
    crecimiento_gastos = 7.0

else:
    crecimiento_ventas = 5.0
    crecimiento_costos = 3.0
    variacion_precio = 2.0
    crecimiento_gastos = 3.0


st.sidebar.subheader("Variables financieras")

unidades = st.sidebar.number_input(
    "Unidades vendidas iniciales",
    min_value=0,
    value=100000,
    step=1000
)

precio = st.sidebar.number_input(
    "Precio por unidad ($)",
    min_value=0.0,
    value=2.0,
    step=0.10
)

costo_unitario = st.sidebar.number_input(
    "Costo variable por unidad ($)",
    min_value=0.0,
    value=0.80,
    step=0.05
)

costos_fijos = st.sidebar.number_input(
    "Costos fijos anuales ($)",
    min_value=0.0,
    value=45000.0,
    step=1000.0
)

gastos = st.sidebar.number_input(
    "Gastos administrativos ($)",
    min_value=0.0,
    value=20000.0,
    step=1000.0
)

st.sidebar.subheader("Supuestos del escenario")

crecimiento_ventas = st.sidebar.slider(
    "Crecimiento anual de ventas (%)",
    -20.0,
    30.0,
    crecimiento_ventas,
    1.0
)

crecimiento_costos = st.sidebar.slider(
    "Crecimiento anual de costos (%)",
    -10.0,
    20.0,
    crecimiento_costos,
    1.0
)

variacion_precio = st.sidebar.slider(
    "Variación anual del precio (%)",
    -10.0,
    20.0,
    variacion_precio,
    1.0
)

crecimiento_gastos = st.sidebar.slider(
    "Crecimiento anual de gastos (%)",
    -10.0,
    20.0,
    crecimiento_gastos,
    1.0
)

# ---------------------------------------------------------
# PESTEL
# ---------------------------------------------------------

st.header("🌎 Análisis PESTEL Prospectivo")

st.write(
    "Califique cada variable de 1 a 3. "
    "1 = Bajo, 2 = Medio y 3 = Alto."
)

variables_pestel = [
    ("Cambios regulatorios", "GASTOS", 3),
    ("Inflación", "COSTOS", 5),
    ("Preferencia por agua purificada", "VENTAS", 8),
    ("Tecnología de purificación", "COSTOS", -4),
    ("Escasez de agua", "VENTAS", -10),
    ("Exigencias sanitarias", "GASTOS", 4)
]

resultados_pestel = []

for variable, tipo, variacion in variables_pestel:

    st.subheader(variable)

    col1, col2 = st.columns(2)

    impacto = col1.slider(
        f"Impacto - {variable}",
        1,
        3,
        2,
        key=f"impacto_{variable}"
    )

    incertidumbre = col2.slider(
        f"Incertidumbre - {variable}",
        1,
        3,
        2,
        key=f"incertidumbre_{variable}"
    )

    criticidad = impacto * incertidumbre

    if criticidad >= 6:
        clasificacion = "CRÍTICO"
        efecto_activo = variacion
    elif criticidad >= 3:
        clasificacion = "MEDIO"
        efecto_activo = 0
    else:
        clasificacion = "BAJO"
        efecto_activo = 0

    resultados_pestel.append({
        "Variable": variable,
        "Impacto": impacto,
        "Incertidumbre": incertidumbre,
        "Criticidad": criticidad,
        "Clasificación": clasificacion,
        "Tipo": tipo,
        "Variación": variacion,
        "Efecto activo": efecto_activo
    })


df_pestel = pd.DataFrame(resultados_pestel)

st.subheader("Resultado PESTEL")

st.dataframe(
    df_pestel[
        [
            "Variable",
            "Impacto",
            "Incertidumbre",
            "Criticidad",
            "Clasificación"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------------------------
# EFECTOS PESTEL
# ---------------------------------------------------------

efecto_ventas = (
    df_pestel[df_pestel["Tipo"] == "VENTAS"]["Efecto activo"].sum()
)

efecto_costos = (
    df_pestel[df_pestel["Tipo"] == "COSTOS"]["Efecto activo"].sum()
)

efecto_gastos = (
    df_pestel[df_pestel["Tipo"] == "GASTOS"]["Efecto activo"].sum()
)

variables_criticas = (
    df_pestel["Clasificación"] == "CRÍTICO"
).sum()

indice_riesgo = df_pestel["Criticidad"].mean()

if indice_riesgo >= 6:
    nivel_riesgo = "ALTO"
elif indice_riesgo >= 3:
    nivel_riesgo = "MEDIO"
else:
    nivel_riesgo = "BAJO"


# ---------------------------------------------------------
# TASAS AJUSTADAS
# ---------------------------------------------------------

tasa_ventas = (
    (1 + crecimiento_ventas / 100)
    * (1 + efecto_ventas / 100)
    - 1
)

tasa_costos = (
    (1 + crecimiento_costos / 100)
    * (1 + efecto_costos / 100)
    - 1
)

tasa_gastos = (
    (1 + crecimiento_gastos / 100)
    * (1 + efecto_gastos / 100)
    - 1
)

tasa_precio = variacion_precio / 100


# ---------------------------------------------------------
# PROYECCIÓN FINANCIERA
# ---------------------------------------------------------

proyeccion = []

u = unidades
p = precio
cu = costo_unitario
g = gastos

for anio in range(1, 6):

    if anio > 1:
        u = u * (1 + tasa_ventas)
        p = p * (1 + tasa_precio)
        cu = cu * (1 + tasa_costos)
        g = g * (1 + tasa_gastos)

    ingresos = u * p
    costos_variables = u * cu
    flujo = ingresos - costos_variables - costos_fijos - g

    proyeccion.append({
        "Año": f"Año {anio}",
        "Unidades": u,
        "Precio": p,
        "Ingresos": ingresos,
        "Costos variables": costos_variables,
        "Costos fijos": costos_fijos,
        "Gastos": g,
        "Flujo operativo": flujo
    })


df = pd.DataFrame(proyeccion)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

st.header("📈 Dashboard Prospectivo Financiero")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Escenario",
    escenario
)

c2.metric(
    "Nivel de riesgo",
    nivel_riesgo
)

c3.metric(
    "Variables críticas",
    int(variables_criticas)
)

c4.metric(
    "Índice de riesgo",
    f"{indice_riesgo:.2f}"
)

c5, c6, c7 = st.columns(3)

c5.metric(
    "Efecto PESTEL Ventas",
    f"{efecto_ventas:.1f}%"
)

c6.metric(
    "Efecto PESTEL Costos",
    f"{efecto_costos:.1f}%"
)

c7.metric(
    "Efecto PESTEL Gastos",
    f"{efecto_gastos:.1f}%"
)


st.subheader("Proyección financiera a 5 años")

st.dataframe(
    df.style.format({
        "Unidades": "{:,.0f}",
        "Precio": "${:,.2f}",
        "Ingresos": "${:,.2f}",
        "Costos variables": "${:,.2f}",
        "Costos fijos": "${:,.2f}",
        "Gastos": "${:,.2f}",
        "Flujo operativo": "${:,.2f}"
    }),
    use_container_width=True
)


# ---------------------------------------------------------
# GRÁFICOS
# ---------------------------------------------------------

st.subheader("Evolución financiera")

st.line_chart(
    df.set_index("Año")[
        [
            "Ingresos",
            "Costos variables",
            "Flujo operativo"
        ]
    ]
)

st.subheader("Criticidad de variables PESTEL")

st.bar_chart(
    df_pestel.set_index("Variable")["Criticidad"]
)


# ---------------------------------------------------------
# ANÁLISIS AUTOMÁTICO
# ---------------------------------------------------------

st.header("🧠 Análisis automático")

flujo_inicial = df.iloc[0]["Flujo operativo"]
flujo_final = df.iloc[-1]["Flujo operativo"]

if flujo_final > flujo_inicial:
    st.success(
        "La situación financiera proyectada presenta una mejora. "
        "El flujo operativo del Año 5 supera al flujo del Año 1."
    )
else:
    st.warning(
        "La situación financiera proyectada presenta un deterioro. "
        "El flujo operativo del Año 5 es inferior al flujo del Año 1."
    )

if nivel_riesgo == "ALTO":
    st.error(
        "El entorno prospectivo presenta un nivel de riesgo alto. "
        "Se recomienda analizar las variables críticas y establecer "
        "estrategias de mitigación."
    )

elif nivel_riesgo == "MEDIO":
    st.warning(
        "El entorno presenta un nivel de riesgo moderado. "
        "Se recomienda realizar seguimiento periódico de las "
        "variables de mayor impacto e incertidumbre."
    )

else:
    st.success(
        "El entorno presenta un nivel de riesgo bajo. "
        "Se recomienda mantener vigilancia prospectiva."
    )
