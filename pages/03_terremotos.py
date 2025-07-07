import streamlit as st
import pandas as pd
import requests
from io import StringIO
import re
import plotly.express as px
import numpy as np

def extraer_pais(texto):
    match = re.match(r'^([^:]+)', texto)
    return match.group(1).strip() if match else texto

def extraer_localidad(texto):
    match = re.search(r':\s*([^,;:]+)', str(texto))
    return match.group(1).strip() if match else None
    
def leer_csv_desde_url(url, sep=',', encoding='utf-8'):
    try:
        response = requests.get(url)
        response.raise_for_status() # Lanza una excepción para códigos de estado HTTP 4xx/5xx
        content = response.content.decode(encoding)
        csv_data = StringIO(content)
        df = pd.read_csv(csv_data, sep=sep)
        return df

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error de red o al acceder a la URL: {e}")
    except pd.errors.EmptyDataError:
        raise Exception("Error: El archivo CSV está vacío o solo contiene encabezados.")
    except pd.errors.ParserError as e:
        raise Exception(f"Error de análisis CSV. Revisa el delimitador (sep) o el formato del archivo: {e}")
    except Exception as e:
        raise Exception(f"Ocurrió un error inesperado: {e}")

url = "https://drive.google.com/uc?export=download&id=1UyX7sRATSNbadNxUZ7AAmbeOUm7sVpGF"
df = leer_csv_desde_url(url)
#df['mag'] = df['Magnitude'] ** 2


opciones = ['Magnitud','Daños','Muertes']
opcion = st.sidebar.selectbox('Seleccionar opción:',opciones)
   
top = st.sidebar.select_slider('Seleccionar TOP', [1,3,5,10,20,25,50,75,100])
# ['1', '3', '5','10','20','30','40','50','60','70','80','90','100']
# [1,3,5,10,20,25,50,75,100]

#df.nlargest(1, ['Magnitude']) 
mag_agno = df.nlargest(1, ['Magnitude'])['Year'].iloc[0]
mag_valor = df.nlargest(1, ['Magnitude'])['Magnitude'].iloc[0]
mag_ubicacion = extraer_pais(df.nlargest(1, ['Magnitude'])['Location_Name'].iloc[0]) + ", " + extraer_localidad(df.nlargest(1, ['Magnitude'])['Location_Name'].iloc[0])

#df.nlargest(1, ['Damage']) 
dmg_agno = df.nlargest(1, ['Damage'])['Year'].iloc[0]
dmg_valor = df.nlargest(1, ['Damage'])['Damage'].iloc[0]
dmg_ubicacion = extraer_pais(df.nlargest(1, ['Damage'])['Location_Name'].iloc[0]) + ", " + extraer_localidad(df.nlargest(1, ['Damage'])['Location_Name'].iloc[0])

#df.nlargest(1, ['Death']) 
dth_agno = df.nlargest(1, ['Death'])['Year'].iloc[0]
dth_valor = df.nlargest(1, ['Death'])['Death'].iloc[0]
dth_ubicacion = extraer_pais(df.nlargest(1, ['Death'])['Location_Name'].iloc[0]) + ", " + extraer_localidad(df.nlargest(1, ['Death'])['Location_Name'].iloc[0])



c1, c2, c3 = st.columns(3)

c1.metric(f"Mayor Magnitud año: {mag_agno}",mag_valor, mag_ubicacion) 
c2.metric(f"Mayor Daño año: {dmg_agno}",dmg_valor, f"-{dmg_ubicacion}") 
c3.metric(f"Mayor Muerte año: {dth_agno}",dth_valor, f"-{dth_ubicacion}") 

if opcion == "Magnitud":
    opcion = "Magnitude"
elif opcion == "Daños":
    opcion = "Damage"
else:
    opcion = "Death"
    
dfx = df.nlargest(top, [opcion])
dfx['mag'] = np.exp(dfx['Magnitude'] - 7) * 3
#np.log1p(df['Magnitude']) *10

if opcion == "Magnitude":
    size = "mag"
elif opcion == "Damage":
    size = "Damage"
else:
    size = "Death"

#st.write(opcion)    
#st.write(dfx) 

fig = px.scatter_mapbox(
    dfx,
    lat="Latitude",
    lon="Longitude",
    size=size,            # <-- ¡Aquí es donde defines la proporcionalidad del tamaño!
    #color=opcion,                  # Puedes colorear por Comuna, Región, o un rango de puntajes
    hover_name="Location_Name",             # Texto que aparece al pasar el ratón por encima
    hover_data={                     # Datos adicionales a mostrar en el tooltip
        "Year": True,
        opcion: True,
        "mag":False,
        "Latitude": False,            # No mostrar lat/lon en el tooltip
        "Longitude": False
    },
    zoom=1,                          # Nivel de zoom inicial
    height=600,
    mapbox_style="carto-positron",   # Estilo del mapa (puedes probar "open-street-map", "stamen-toner", etc.)
    size_max=30                      # Tamaño máximo de los puntos en el mapa
)


# Actualizar el layout para ajustar márgenes y centrar el mapa
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True)




