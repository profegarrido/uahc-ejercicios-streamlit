import streamlit as st
import pandas as pd
import requests
from io import StringIO


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

url = "https://raw.githubusercontent.com/lgarridocornejo/uacademia/refs/heads/master/modulo_03/concap.csv"
df = leer_csv_desde_url(url)


continentes = sorted(list(df["ContinentName"].unique()))
continente = st.sidebar.selectbox('Seleccionar Continente:',continentes)

paises = sorted(df[df['ContinentName'] == continente]['CountryName'].unique())
pais = st.sidebar.selectbox('Seleccionar Pais:',paises)

capital = sorted(df[df['CountryName'] == pais]['CapitalName'].unique())
st.sidebar.code(capital[0])


dfx = df[(df['CapitalName'] == capital[0]) & (df['CountryName'] == pais)]
#st.write(dfx)

st.map(dfx, latitude="CapitalLatitude", longitude="CapitalLongitude")