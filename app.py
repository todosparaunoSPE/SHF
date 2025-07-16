# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 18:06:39 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Demo Analista de Operación", layout="wide")

# Título
st.title("🏦 Demo Técnica: Análisis de Productos de Garantía")
st.markdown("**Ejemplo práctico de las capacidades requeridas para el puesto**")

# Dividir en pestañas
tab1, tab2, tab3 = st.tabs(["Validación de Cálculos", "Detección de Desviaciones", "Carga de Sistemas"])

## TAB 1: Validación de cálculos de contraprestación
with tab1:
    st.header("🔢 Validación de Cálculos de Garantías")
    st.write("""
    **Objetivo:** Verificar la correcta aplicación de fórmulas financieras para productos de garantía.
    """)
    
    # Simular datos de garantías
    @st.cache_data
    def generar_datos_garantias():
        np.random.seed(42)
        fechas = pd.date_range(start="2024-01-01", end="2024-12-31", periods=100)
        datos = pd.DataFrame({
            "ID Garantía": [f"G-{1000+i}" for i in range(100)],
            "Fecha Emisión": fechas,
            "Monto Asegurado": np.round(np.random.uniform(50000, 500000, 100), 2),
            "Plazo (meses)": np.random.choice([12, 24, 36, 60], 100),
            "Tasa Anual": np.round(np.random.uniform(0.08, 0.15, 100), 4),
            "Contraprestación Calculada": np.round(np.random.uniform(1000, 20000, 100), 2)
        })
        
        # Calcular contraprestación correcta (fórmula simplificada)
        datos["Contraprestación Correcta"] = np.round(
            datos["Monto Asegurado"] * datos["Tasa Anual"] / 12 * datos["Plazo (meses)"], 2)
        
        # Introducir algunos errores aleatorios
        errores = np.random.choice([0, 1], 100, p=[0.85, 0.15])
        datos.loc[errores == 1, "Contraprestación Calculada"] = datos.loc[errores == 1, "Contraprestación Correcta"] * np.random.uniform(0.8, 1.2, sum(errores))
        
        return datos

    datos_garantias = generar_datos_garantias()
    
    # Mostrar tabla con errores resaltados
    st.subheader("Revisión de Contraprestaciones")
    
    # Calcular diferencia porcentual
    datos_garantias["Diferencia"] = datos_garantias["Contraprestación Calculada"] - datos_garantias["Contraprestación Correcta"]
    datos_garantias["% Dif"] = datos_garantias["Diferencia"] / datos_garantias["Contraprestación Correcta"] * 100
    
    # Filtrar solo las que tienen error significativo (>1%)
    errores = datos_garantias[np.abs(datos_garantias["% Dif"]) > 1]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Garantías", len(datos_garantias))
    with col2:
        st.metric("Garantías con Error", len(errores), delta=f"{len(errores)/len(datos_garantias)*100:.1f}%")
    
    # Función para resaltar errores
    def highlight_errors(row):
        color = 'background-color: #ffcccc' if abs(row["% Dif"]) > 5 else ''
        return [color] * len(row)
    
    # Mostrar tabla con errores resaltados
    st.dataframe(
        errores.style.apply(highlight_errors, axis=1)
    )
    
    # Explicación del análisis
    with st.expander("🔍 Análisis Matemático Detallado"):
        st.write("""
        **Fórmula aplicada para validación:**
        ```
        Contraprestación Correcta = Monto Asegurado × (Tasa Anual / 12) × Plazo en Meses
        ```
        
        Como matemático, puedo:
        - Verificar la correcta aplicación de fórmulas financieras
        - Identificar errores de redondeo o cálculo
        - Desarrollar algoritmos para validación automática
        - Optimizar los cálculos para grandes volúmenes de datos
        """)

## TAB 2: Detección de desviaciones
with tab2:
    st.header("📈 Detección de Desviaciones Operativas")
    st.write("""
    **Objetivo:** Identificar patrones inusuales en la operación de garantías.
    """)
    
    # Análisis de series de tiempo
    st.subheader("Tendencia Mensual de Montos Asegurados")
    
    # Agrupar por mes
    datos_garantias["Mes"] = datos_garantias["Fecha Emisión"].dt.to_period("M").astype(str)
    mensual = datos_garantias.groupby("Mes").agg({
        "Monto Asegurado": ["count", "sum", "mean"],
        "% Dif": "mean"
    }).reset_index()
    
    # Aplanar las columnas multi-nivel para Streamlit
    mensual.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in mensual.columns.values]
    
    # Renombrar las columnas para que sea más claro
    mensual = mensual.rename(columns={
        'Mes_': 'Mes',
        'Monto Asegurado_count': 'Cantidad_Garantias',
        'Monto Asegurado_sum': 'Monto_Total',
        'Monto Asegurado_mean': 'Monto_Promedio',
        '% Dif_mean': 'Error_Promedio'
    })
    
    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Monto Total Mensual")
        st.line_chart(mensual.set_index("Mes")["Monto_Total"])
    with col2:
        st.subheader("Cantidad de Garantías Mensuales")
        st.bar_chart(mensual.set_index("Mes")["Cantidad_Garantias"])
    
    # Mostrar tabla resumen
    st.subheader("Resumen Estadístico Mensual")
    st.dataframe(mensual)
    
    # Detección de outliers
    st.subheader("Detección de Valores Atípicos")
    
    q1 = datos_garantias["Monto Asegurado"].quantile(0.25)
    q3 = datos_garantias["Monto Asegurado"].quantile(0.75)
    iqr = q3 - q1
    
    outliers = datos_garantias[
        (datos_garantias["Monto Asegurado"] < (q1 - 1.5*iqr)) | 
        (datos_garantias["Monto Asegurado"] > (q3 + 1.5*iqr))
    ]
    
    st.write(f"Se detectaron {len(outliers)} operaciones con montos atípicos:")
    st.dataframe(outliers[["ID Garantía", "Fecha Emisión", "Monto Asegurado"]])
    
    with st.expander("🧮 Métodos Estadísticos Aplicados"):
        st.write("""
        - **Rango intercuartílico (IQR):** Método robusto para detección de outliers
        - **Análisis de tendencias:** Identificación de patrones temporales
        - **Comparativa con medias móviles:** Detección de desviaciones significativas
        """)

## TAB 3: Carga de sistemas
with tab3:
    st.header("💾 Simulación de Carga a Sistemas Institucionales")
    st.write("""
    **Objetivo:** Verificar la integridad de los datos al cargarse a sistemas.
    """)
    
    # Simular proceso de carga
    st.subheader("Validación Pre-Carga")
    
    # Mostrar datos a cargar
    st.write("Datos a cargar al sistema:")
    st.dataframe(datos_garantias.head(5))
    
    # Verificar integridad
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Registros a Cargar", len(datos_garantias))
    with col2:
        st.metric("Campos por Registro", len(datos_garantias.columns))
    with col3:
        nulos = datos_garantias.isnull().sum().sum()
        st.metric("Valores Nulos Detectados", nulos, delta_color="inverse")
    
    # Simular carga
    if st.button("🔽 Simular Carga al Sistema"):
        with st.spinner("Procesando carga..."):
            # Simular validación
            if nulos > 0:
                st.error("❌ Error: No se puede cargar - Existen valores nulos")
            else:
                # Simular transformación de datos
                datos_cargados = datos_garantias.copy()
                datos_cargados["Fecha Carga"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                datos_cargados["Usuario"] = "DEMO_USER"
                
                st.success("✅ Carga exitosa - 100% de registros procesados")
                st.download_button(
                    label="Descargar Log de Carga",
                    data=datos_cargados.to_csv(index=False).encode("utf-8"),
                    file_name="log_carga_garantias.csv",
                    mime="text/csv"
                )
    
    with st.expander("⚙️ Automatización Propuesta"):
        st.write("""
        Como experto en ciencias de la computación, propongo:
        - **Scripts de validación automática** (Python) para:
          - Chequeo de integridad referencial
          - Validación de rangos y formatos
          - Consistencia temporal
        - **Registros de auditoría** detallados
        - **Procesos ETL** robustos para transferencia de datos
        """)

# Nota final
st.markdown("---")
st.markdown("""
**Demostración técnica creada por: Javier Horacio Pérez Ricárdez**  
Matemático con Maestría en Ciencias de la Computación  
*Herramientas utilizadas: Python, Pandas, Streamlit, Análisis Estadístico*
""")