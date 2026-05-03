import streamlit as st
import pandas as pd
import os

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
st.set_page_config(page_title="Smart Finance App", layout="wide")

# -----------------------------
# ESTADOS
# -----------------------------
for key in ["movimientos", "productos", "historial_funciones", "registros_crud"]:
    if key not in st.session_state:
        st.session_state[key] = []

# -----------------------------
# FUNCIONES
# -----------------------------
def calcular_interes(capital, tasa, tiempo):
    return capital * (1 + tasa) ** tiempo

# -----------------------------
# CLASE
# -----------------------------
class Cliente:
    def __init__(self, nombre, edad, saldo):
        self.nombre = nombre
        self.edad = edad
        self.saldo = saldo

# -----------------------------
# MENÚ
# -----------------------------
menu = st.sidebar.selectbox("Menú", [
    "Home",
    "Ejercicio 1",
    "Ejercicio 2",
    "Ejercicio 3",
    "Ejercicio 4"
])

# -----------------------------
# HOME
# -----------------------------
if menu == "Home":
    st.title("🚀 Smart Finance App")
    st.subheader("Sistema inteligente de gestión y análisis financiero")

    col1, col2 = st.columns(2)

    # 🔥 FIX DEFINITIVO DE LA IMAGEN
    BASE_DIR = os.path.dirname(__file__)
    ruta_imagen = os.path.join(BASE_DIR, "dmc.png")

    if os.path.exists(ruta_imagen):
        col1.image(ruta_imagen, width=150)
    else:
        col1.warning("⚠️ Imagen no encontrada")

    st.markdown("---")

    st.write("👤 **Nombre:** Jesus Alexander Ortiz Cahuana")
    st.write("📚 **Módulo:** Python Fundamentals")
    st.write("🎓 **Especialización:** Python for Analytics")
    st.write("📅 **Año:** 2026")

    st.markdown("""
    ### 📌 Descripción
    Aplicación interactiva desarrollada en Streamlit que integra:
    - Variables
    - Estructuras de datos
    - Control de flujo
    - Funciones
    - Programación orientada a objetos
    """)

# -----------------------------
# EJERCICIO 1
# -----------------------------
elif menu == "Ejercicio 1":
    st.title("Ejercicio 1 - Flujo de Caja")

    with st.form("form_movimientos"):
        col1, col2, col3 = st.columns(3)

        concepto = col1.text_input("Concepto")
        tipo = col2.selectbox("Tipo", ["Ingreso", "Gasto"])
        valor = col3.number_input("Valor", min_value=0.0)

        submitted = st.form_submit_button("Agregar")

    if submitted:
        if concepto == "" or valor == 0:
            st.warning("Completa los datos")
        else:
            st.session_state.movimientos.append({
                "Concepto": concepto,
                "Tipo": tipo,
                "Valor": valor
            })

    df = pd.DataFrame(st.session_state.movimientos)

    if not df.empty:
        st.dataframe(df)

        ingresos = df[df["Tipo"] == "Ingreso"]["Valor"].sum()
        gastos = df[df["Tipo"] == "Gasto"]["Valor"].sum()

        st.metric("Saldo", ingresos - gastos)

        df["Acumulado"] = df["Valor"].cumsum()
        st.line_chart(df["Acumulado"])

# -----------------------------
# EJERCICIO 2
# -----------------------------
elif menu == "Ejercicio 2":
    st.title("Ejercicio 2 - Registro de Productos")

    with st.form("form_productos"):
        nombre = st.text_input("Producto")
        categoria = st.selectbox("Categoría", ["Tecnología", "Ropa", "Otros"])
        precio = st.number_input("Precio", min_value=0.0)
        cantidad = st.number_input("Cantidad", min_value=0)

        submitted = st.form_submit_button("Agregar")

    if submitted:
        if nombre == "" or precio == 0 or cantidad == 0:
            st.warning("Datos inválidos")
        else:
            total = precio * cantidad
            st.session_state.productos.append({
                "Producto": nombre,
                "Categoría": categoria,
                "Total": total
            })

    df = pd.DataFrame(st.session_state.productos)

    if not df.empty:
        st.dataframe(df)
        st.bar_chart(df.groupby("Categoría")["Total"].sum())

# -----------------------------
# EJERCICIO 3
# -----------------------------
elif menu == "Ejercicio 3":
    st.title("Ejercicio 3 - Cálculo de Interés")

    capital = st.number_input("Capital", min_value=0.0)
    tasa = st.number_input("Tasa", min_value=0.0)
    tiempo = st.number_input("Tiempo", min_value=0)

    if st.button("Calcular"):
        if capital == 0 or tasa == 0 or tiempo == 0:
            st.warning("Completa los datos")
        else:
            resultado = calcular_interes(capital, tasa, tiempo)
            st.success(f"Resultado: {resultado:.2f}")

            st.session_state.historial_funciones.append({
                "Resultado": resultado
            })

    df = pd.DataFrame(st.session_state.historial_funciones)

    if not df.empty:
        st.dataframe(df)
        st.line_chart(df["Resultado"])

# -----------------------------
# EJERCICIO 4
# -----------------------------
elif menu == "Ejercicio 4":
    st.title("Ejercicio 4 - CRUD Clientes")

    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", min_value=0)
    saldo = st.number_input("Saldo", min_value=0.0)

    if st.button("Crear"):
        if nombre == "":
            st.warning("Nombre requerido")
        else:
            cliente = Cliente(nombre, edad, saldo)
            st.session_state.registros_crud.append(cliente.__dict__)

    df = pd.DataFrame(st.session_state.registros_crud)

    if not df.empty:
        st.dataframe(df)

        idx = st.number_input("Eliminar índice", min_value=0, max_value=len(df)-1)

        if st.button("Eliminar"):
            st.session_state.registros_crud.pop(idx)
            st.rerun()