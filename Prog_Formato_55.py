import streamlit as st
import pandas as pd
import os

def procesar_archivos(archivo_formato_55, archivo_cartera_90_360, archivo_cartera_90):
    # Cargar los CSVs
    df_55 = pd.read_csv(archivo_formato_55, dtype=str)
    df_90_360 = pd.read_csv(archivo_cartera_90_360, dtype=str)
    df_90 = pd.read_csv(archivo_cartera_90, dtype=str)
    
    # Normalizar nombres de columnas
    for df in [df_55, df_90_360, df_90]:
        df.columns = df.columns.str.strip().str.upper()
    
    # Convertir columnas a numérico
    df_90_360['SALDO_FACTURA'] = pd.to_numeric(df_90_360['SALDO_FACTURA'], errors='coerce').fillna(0)
    df_90['SALDO_FACTURA'] = pd.to_numeric(df_90['SALDO_FACTURA'], errors='coerce').fillna(0)
    df_55['SALDO_CAR_90A360'] = pd.to_numeric(df_55['SALDO_CAR_90A360'], errors='coerce').fillna(0)
    df_55['SALDO_CAR_90'] = pd.to_numeric(df_55['SALDO_CAR_90'], errors='coerce').fillna(0)
    
    # Crear diccionarios de mapeo
    mapeo_90_360 = df_90_360.set_index('COD_LOCALIDAD')['SALDO_FACTURA'].to_dict()
    mapeo_90 = df_90.set_index('COD_LOCALIDAD')['SALDO_FACTURA'].to_dict()
    
    # Actualizar valores en df_55
    df_55['SALDO_CAR_90A360'] += df_55['COD_LOCALIDAD'].map(mapeo_90_360).fillna(0)
    df_55['SALDO_CAR_90'] += df_55['COD_LOCALIDAD'].map(mapeo_90).fillna(0)
    
    # Caso especial COD_LOCALIDAD == "4443000000001"
    df_55.loc[df_55['COD_LOCALIDAD'] == "4443000000001", 'SALDO_CAR_90A360'] += mapeo_90_360.get("4443000000001", 0) / 4
    df_55.loc[df_55['COD_LOCALIDAD'] == "4443000000001", 'SALDO_CAR_90'] += mapeo_90.get("4443000000001", 0) / 4
    
    # Generar nombre del archivo de salida
    nombre_salida = f"ZNISISFV_64716_54_{os.path.basename(archivo_formato_55.name)}"
    df_55.to_csv(nombre_salida, index=False)
    
    return nombre_salida

st.title("Generar Formato IUF1")

st.subheader("Cargar archivo de la Mora")
archivo_cartera_90_360 = st.file_uploader("Subir archivo Cartera 90-360", type=["csv"], key="cartera_90_360")

st.subheader("Cargar archivo a actualizar")
archivo_formato_55 = st.file_uploader("Subir archivo Formato 55", type=["csv"], key="formato_55")

st.subheader("Cargar archivo Cartera 90")
archivo_cartera_90 = st.file_uploader("Subir archivo Cartera 90", type=["csv"], key="cartera_90")

if st.button("Procesar Archivos"):
    if archivo_formato_55 and archivo_cartera_90_360 and archivo_cartera_90:
        nombre_salida = procesar_archivos(archivo_formato_55, archivo_cartera_90_360, archivo_cartera_90)
        st.success(f"Archivo generado: {nombre_salida}")
        with open(nombre_salida, "rb") as f:
            st.download_button("Descargar Archivo", f, file_name=nombre_salida)
    else:
        st.error("Por favor, suba los tres archivos CSV.")
