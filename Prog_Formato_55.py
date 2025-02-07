import streamlit as st
import pandas as pd
import io

# Configuración inicial
st.title("Procesamiento de Archivos CSV")
st.markdown("Sube los archivos para generar el archivo procesado.")

# Cargar archivos desde la interfaz de usuario
archivo_formato_55 = st.file_uploader("Sube Formato_55_Nov_2024.csv", type=["csv"])
archivo_cartera_90_360 = st.file_uploader("Sube Cartera_90_360_Nov_2024.csv", type=["csv"])
archivo_cartera_90 = st.file_uploader("Sube Cartera_90_Nov_2024.csv", type=["csv"])

# Verificar si se han subido todos los archivos
if archivo_formato_55 and archivo_cartera_90_360 and archivo_cartera_90:
    
    if st.button("Procesar Archivos"):
        # Leer los archivos
        df_formato_55 = pd.read_csv(archivo_formato_55, dtype=str)
        df_cartera_90_360 = pd.read_csv(archivo_cartera_90_360, dtype=str)
        df_cartera_90 = pd.read_csv(archivo_cartera_90, dtype=str)

        # Normalizar nombres de columnas
        df_formato_55.columns = df_formato_55.columns.str.strip().str.upper()
        df_cartera_90_360.columns = df_cartera_90_360.columns.str.strip().str.upper()
        df_cartera_90.columns = df_cartera_90.columns.str.strip().str.upper()

        # Convertir las columnas numéricas
        df_formato_55['SALDO_CAR_90A360'] = pd.to_numeric(df_formato_55['SALDO_CAR_90A360'], errors='coerce').fillna(0)
        df_formato_55['SALDO_CAR_90'] = pd.to_numeric(df_formato_55['SALDO_CAR_90'], errors='coerce').fillna(0)
        df_cartera_90_360['SALDO_FACTURA'] = pd.to_numeric(df_cartera_90_360['SALDO_FACTURA'], errors='coerce').fillna(0)
        df_cartera_90['SALDO_FACTURA'] = pd.to_numeric(df_cartera_90['SALDO_FACTURA'], errors='coerce').fillna(0)

        # Crear diccionarios de mapeo por COD_LOCALIDAD
        mapeo_saldo_90_360 = df_cartera_90_360.set_index('COD_LOCALIDAD')['SALDO_FACTURA'].to_dict()
        mapeo_saldo_90 = df_cartera_90.set_index('COD_LOCALIDAD')['SALDO_FACTURA'].to_dict()

        # Función para actualizar los saldos
        def actualizar_saldos(row):
            cod_localidad = row['COD_LOCALIDAD']
            
            # Obtener los valores de saldo
            saldo_90_360 = mapeo_saldo_90_360.get(cod_localidad, 0)
            saldo_90 = mapeo_saldo_90.get(cod_localidad, 0)
            
            # Aplicar la lógica de división para el caso especial
            if cod_localidad == "4443000000001":
                row['SALDO_CAR_90A360'] += saldo_90_360 / 4
                row['SALDO_CAR_90'] += saldo_90 / 4
            else:
                row['SALDO_CAR_90A360'] += saldo_90_360
                row['SALDO_CAR_90'] += saldo_90
            
            return row

        # Aplicar la función a cada fila del DataFrame
        df_formato_55 = df_formato_55.apply(actualizar_saldos, axis=1)

        # Guardar el resultado en memoria para descarga
        output = io.BytesIO()
        df_formato_55.to_csv(output, index=False, encoding="utf-8")
        output.seek(0)

        # Botón de descarga
        st.download_button(
            label="Descargar Archivo Procesado",
            data=output,
            file_name="ZNISISFV_64716_55_112024.csv",
            mime="text/csv"
        )

        st.success("Procesamiento completado. Descarga el archivo.")