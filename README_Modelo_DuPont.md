# 📊 Modelo DuPont en Streamlit

Esta aplicación permite cargar una base de datos financiera en formato Excel y calcular los principales indicadores del modelo DuPont para distintos períodos.

## 🚀 Indicadores calculados

- Margen Neto (%)
- Rotación (veces)
- Apalancamiento (veces)
- ROE (Retorno sobre Capital)
- ROA (Retorno sobre Activos)
- Pay Back Capital (veces)
- Pay Back Activos (veces)

Incluye una columna de variación porcentual (**v%**) entre los dos últimos periodos.

## 📂 Estructura esperada del Excel

El archivo debe contener las siguientes columnas:

- `Periodo`
- `Utilidad Neta`
- `Ventas Netas`
- `Activos Totales`
- `Capital Contable`

## ▶️ Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Despliegue

Puedes desplegarlo fácilmente en [Streamlit Cloud](https://streamlit.io/cloud). Solo sube estos archivos a un repositorio y conecta tu cuenta.

---

Desarrollado para análisis financiero profesional y educativo.