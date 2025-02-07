import streamlit as st
import pandas as pd
import io

def procesar_archivos(formato_55, cartera_90_360, cartera_90):
    # Cargar los archivos CSV
    df_formato_55 = pd.read_csv(formato_55, dtype=str)
    df_cartera_90_360 = pd.read_csv(cartera_90_360, dtype=str)
    df_cartera_90 = pd.read_csv(cartera_90, dtype=str)
    
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
        saldo_90_360 = mapeo_saldo_90_360.get(cod_localidad, 0)
        saldo_90 = mapeo_saldo_90.get(cod_localidad, 0)
        if cod_localidad == "4443000000001":
            row['SALDO_CAR_90A360'] += saldo_90_360 / 4
            row['SALDO_CAR_90'] += saldo_90 / 4
        else:
            row['SALDO_CAR_90A360'] += saldo_90_360
            row['SALDO_CAR_90'] += saldo_90
        return row
    
    # Aplicar la función a cada fila del DataFrame
    df_formato_55 = df_formato_55.apply(actualizar_saldos, axis=1)
    
    # Guardar el resultado en memoria
    output = io.BytesIO()
    df_formato_55.to_csv(output, index=False, encoding="utf-8")
    output.seek(0)
    return output

st.title("Procesamiento de Archivos CSV")

# Carga de archivos
archivo_formato_55 = st.file_uploader("Cargar archivo Formato_55", type="csv")
archivo_cartera_90_360 = st.file_uploader("Cargar archivo Cartera_90_360", type="csv")
archivo_cartera_90 = st.file_uploader("Cargar archivo Cartera_90", type="csv")

if archivo_formato_55 and archivo_cartera_90_360 and archivo_cartera_90:
    if st.button("Procesar Archivos"):
        archivo_salida = procesar_archivos(archivo_formato_55, archivo_cartera_90_360, archivo_cartera_90)
        st.download_button(
            label="Descargar Archivo Procesado",
            data=archivo_salida,
            file_name="ZNISISFV_64716_55_112024.csv",
            mime="text/csv"
        )
        st.success("Archivo procesado correctamente.")
