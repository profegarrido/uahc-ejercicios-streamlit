import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import StringIO

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def grafico_habilidades(cat):
    categoria = cat
    if cat == 'Ataque':
        habilidad = 'base_attack'
        color = 'tomato'
    elif cat == 'Defensa':
        habilidad = 'base_defense'
        color = '#90EE90'
    else:
        habilidad = 'base_stamina'
        color = 'yellow'
        
    valor = df[habilidad][df['pokemon_id'] == id].item()
    hmax = df[habilidad].max()
    hmed = df[habilidad].mean()

    fig, ax = plt.subplots(figsize=(7, 1))
    ax.barh(categoria, valor, color=color, edgecolor='black', height=0.6)
    ax.axvline(x=hmax, color='red', linestyle='--', linewidth=2, label='máx')
    ax.axvline(x=hmed, color='blue', linestyle='--', linewidth=2, label='media')
#    ax.legend()
    st.pyplot(fig)



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


url = "https://raw.githubusercontent.com/profegarrido/uahc-ejercicios-streamlit/refs/heads/main/pages/pokemon.csv"
df = leer_csv_desde_url(url)  

#df = pd.read_csv('pokemon_final.csv')
csv = df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="Descargar dataset",
    data=csv,
    file_name='pokemon.csv',
    mime='text/csv',
)

tipo =  st.sidebar.selectbox('Seleccionar tipo', df['tipo'].unique().tolist())

subtipo = st.sidebar.selectbox('Seleccionar subtipo', df['subtipo'][df['tipo']==tipo].unique().tolist())

pokemon = st.sidebar.selectbox('Seleccionar pokemon', df['pokemon_name'][(df['tipo'] == tipo) & (df['subtipo'] == subtipo)].unique().tolist())

id = df['pokemon_id'][df['pokemon_name'] == pokemon].iloc[0]

   
resultado = df.loc[df['pokemon_id'] == id, 'imagen']

if not resultado.empty:
    ruta = resultado.iloc[0]
    
    # 2. pd.notna() detecta None, NaN y otros valores nulos
    if pd.notna(ruta) and ruta != "Null":
        st.sidebar.image(ruta, width=150)
#    else:
#        st.sidebar.write("Imagen no disponible")
else:
    st.sidebar.write("Pokémon no encontrado")
#

st.write('Nivel Básico')

nombre = df['pokemon_name']
ataque = df['base_attack'][df['pokemon_id'] == id].item()
defensa = df['base_defense'][df['pokemon_id'] == id].item()
stamina = df['base_stamina'][df['pokemon_id'] == id].item()

#st.title(pokemon)
st.markdown(f"<h1 style='text-align: center;'>{pokemon}</h1>", unsafe_allow_html=True)

st.write('Nivel Medio')
c1, c2, c3 = st.columns(3)

c1.metric(f"Ataque base",ataque, " ") 
c2.metric(f"Defensa base",defensa, "") 
c3.metric(f"Stamina base",stamina, "") 

st.write('Nivel Master')
st.subheader(f"Comparativa de: {pokemon} vs Promedio/Máximo")


grafico_habilidades('Ataque')

grafico_habilidades('Defensa')

grafico_habilidades('Stamina')


