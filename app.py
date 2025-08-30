import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Modelo DuPont", layout="wide")
st.title("📊 Modelo DuPont – Análisis de Rentabilidad")

st.write("Carga un archivo Excel que contenga los campos necesarios para calcular los indicadores por período.")

# Subida de archivo
uploaded_file = st.file_uploader("📂 Cargar archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Vista previa de la base de datos")
    st.dataframe(df)

    columnas_requeridas = ["Periodo", "Utilidad Neta", "Ventas Netas", "Activos Totales", "Capital Contable"]
    if all(col in df.columns for col in columnas_requeridas):

        df = df.copy()
        df["Margen Neto (%)"] = (df["Utilidad Neta"] / df["Ventas Netas"]) * 100
        df["Rotación (veces)"] = df["Ventas Netas"] / df["Activos Totales"]
        df["Apalancamiento (veces)"] = df["Activos Totales"] / df["Capital Contable"]
        df["ROE (%)"] = df["Margen Neto (%)"] * df["Rotación (veces)"] / 100
        df["ROA (%)"] = df["Rotación (veces)"] * df["Apalancamiento (veces)"]
        df["Pay Back Capital (veces)"] = 1 / df["ROE (%)"]
        df["Pay Back Activos (veces)"] = 1 / df["ROA (%)"]

        # Redondeos
        df["Margen Neto (%)"] = df["Margen Neto (%)"].round(1)
        df["ROE (%)"] = df["ROE (%)"].round(1)
        df["ROA (%)"] = df["ROA (%)"].round(1)
        df["Rotación (veces)"] = df["Rotación (veces)"].round(1)
        df["Apalancamiento (veces)"] = df["Apalancamiento (veces)"].round(1)
        df["Pay Back Capital (veces)"] = df["Pay Back Capital (veces)"].round(1)
        df["Pay Back Activos (veces)"] = df["Pay Back Activos (veces)"].round(1)

        # Reorganización de datos
        indicadores = {
            "Margen Neto (%)": "Margen Neto",
            "Rotación (veces)": "Rotación",
            "Apalancamiento (veces)": "Apalancamiento",
            "ROE (%)": "ROE (Retorno Capital)",
            "ROA (%)": "ROA (Retorno Activos)",
            "Pay Back Capital (veces)": "Pay Back Capital",
            "Pay Back Activos (veces)": "Pay Back Activos"
        }

        resultado = pd.DataFrame(index=indicadores.values())

        # Insertar cada periodo como columna
        for periodo in df["Periodo"].unique():
            df_periodo = df[df["Periodo"] == periodo].iloc[0]
            for key, nombre_indicador in indicadores.items():
                resultado.loc[nombre_indicador, periodo] = df_periodo[key]

        # Calcular columna de variación porcentual entre últimos 2 periodos
        periodos = df["Periodo"].unique()
        if len(periodos) >= 2:
            p1, p2 = periodos[-2], periodos[-1]
            resultado["v%"] = ((resultado[p2] - resultado[p1]) / resultado[p1] * 100).round(1)
        else:
            resultado["v%"] = np.nan

        # Mostrar resultados
        st.subheader("📋 Formato Modelo Dupont con variación (%)")
        st.dataframe(resultado)

        # Descarga como Excel
        def to_excel(df):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Modelo Dupont')
            return output.getvalue()

        st.download_button(
            label="📥 Descargar en Excel",
            data=to_excel(resultado),
            file_name="formato_modelo_dupont.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.error("❌ El archivo debe contener: " + ", ".join(columnas_requeridas))
