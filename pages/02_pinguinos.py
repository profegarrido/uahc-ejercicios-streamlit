import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

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


url = "https://drive.google.com/uc?export=download&id=1hExWRWNZZlpkgo8W2r90qkGh8Oc9MRiH"
df = leer_csv_desde_url(url)

st.header("Gráfico Culmen Length / Flipper Length")

especie = st.sidebar.radio(
    "Seleccionar especie",
    ["Adelie Penguin", "Chinstrap penguin", "Gentoo penguin"],
)
 
if especie == "Adelie Penguin":
    especie = "Adelie Penguin (Pygoscelis adeliae)"
elif especie == "Chinstrap penguin":
    especie = "Chinstrap penguin (Pygoscelis antarctica)"
else:
    especie = "Gentoo penguin (Pygoscelis papua)"
    
dfx = df[df['Species'] == especie]
#st.write(dfx)


fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x="Culmen Length (mm)", y="Flipper Length (mm)", data=dfx, hue="Sex")
st.pyplot(fig)



