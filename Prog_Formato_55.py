import streamlit as st
import pandas as pd
import os

st.title("Generar formato 54 - Promail")

# Cargar archivos desde el usuario
archivo1 = st.file_uploader("Cargar archivo de la Mora entre 90 a 360", type=['csv'])
archivo2 = st.file_uploader("Cargar archivo de la Mora menor a 90", type=['csv'])
archivo3 = st.file_uploader("Cargar archivo a actualizar", type=['csv'])

if archivo1 and archivo2 and archivo3:
    if st.button("Realizar Cruce"):
        try:
            # Leer los archivos CSV
            df1 = pd.read_csv(archivo1)
            df2 = pd.read_csv(archivo2)
            df3 = pd.read_csv(archivo3)
            
            # Asegurar que la columna 'Saldo_Factura' sea numérica
            #Convertir columnas a numérico
            df1['SALDO_FACTURA'] = pd.to_numeric(df1['SALDO_FACTURA'], errors='coerce').fillna(0)
            df2['SALDO_FACTURA'] = pd.to_numeric(df2['SALDO_FACTURA'], errors='coerce').fillna(0)
            df3['SALDO_CAR_90A360'] = pd.to_numeric(df3['SALDO_CAR_90A360'], errors='coerce').fillna(0)
            df3['SALDO_CAR_90'] = pd.to_numeric(df3['SALDO_CAR_90'], errors='coerce').fillna(0)
            
            # Crear diccionarios de mapeo
            mapeo_90_360 = df1.set_index('COD_LOCALIDAD')['SALDO_FACTURA'].to_dict()
            mapeo_90 = df2.set_index('COD_LOCALIDAD')['SALDO_FACTURA'].to_dict()
            
            # Actualizar valores en df3
            df3['SALDO_CAR_90A360'] += df3['COD_LOCALIDAD'].map(mapeo_90_360).fillna(0)
            df3['SALDO_CAR_90'] += df3['COD_LOCALIDAD'].map(mapeo_90).fillna(0)
            
            # Caso especial COD_LOCALIDAD == "4443000000001"
            df3.loc[df3['COD_LOCALIDAD'] == "4443000000001", 'SALDO_CAR_90A360'] += mapeo_90_360.get("4443000000001", 0) / 4
            df3.loc[df3['COD_LOCALIDAD'] == "4443000000001", 'SALDO_CAR_90'] += mapeo_90.get("4443000000001", 0) / 4
            
            # Generar nombre del archivo de salida
            nombre_salida = f"ZNISISFV_64716_54_{os.path.basename(archivo_formato_55.name)}"
            df_55.to_csv(nombre_salida, index=False)
    
            # Guardar el resultado en un buffer
            output = io.BytesIO()
            df3.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)
            
            # Obtener el nombre del archivo original y modificarlo
            archivo_nombre = "ZNISISFV_64716_54_" + archivo3.name
            
            # Botón para descargar el archivo actualizado
            st.download_button(label="Descargar archivo actualizado", data=output, file_name=archivo_nombre, mime="text/csv")
            
            st.success("Actualización completada.")
        except Exception as e:
            st.error(f"Error en el procesamiento de los archivos: {e}")