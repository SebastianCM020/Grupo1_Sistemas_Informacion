# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KB5VGFguVOlUiLLtq7lZr4um4Spp3UCC
"""



"""# Proceso ETL: Presión Fiscal del SRI

Este notebook sigue la estructura de un proceso ETL (Extracción, Transformación, Carga) para obtener datos de Presión Fiscal del sitio web del SRI y cargarlos en una hoja de Google Sheets.

## 1. Extracción

La fase de Extracción se encarga de obtener los datos de la fuente original. En este caso, la fuente es una página web del Servicio de Rentas Internas (SRI) de Ecuador.

### Subtarea 1.1: Obtener el contenido de la página web

Descargar el código HTML de la página que contiene el enlace al archivo de datos de Presión Fiscal.

**Razonamiento**:
Utilizamos la biblioteca `requests` para hacer una solicitud GET a la URL de la página web y obtener su contenido HTML. Verificamos el código de estado para asegurar que la solicitud fue exitosa.
"""

import requests

# URL de la página web que contiene el enlace al archivo de datos
url = "https://www.sri.gob.ec/datasets#Presi%C3%B3n%20Fiscal"

try:
    # Realizar la solicitud GET a la página web
    print(f"Intentando obtener el contenido de la página: {url}")
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        html_content = response.text
        print("Contenido de la página web obtenido con éxito.")
    else:
        # Imprimir un mensaje de error si la solicitud no fue exitosa
        print(f"Error al obtener la página. Código de estado: {response.status_code}")
        html_content = None

except requests.exceptions.RequestException as e:
    # Capturar y mostrar cualquier error de conexión o solicitud
    print(f"Ocurrió un error al realizar la solicitud a la página web: {e}")

"""### Subtarea 1.2: Analizar el HTML y encontrar el enlace del archivo CSV

Utilizar una biblioteca como `BeautifulSoup` para parsear el contenido HTML y buscar el enlace de descarga del archivo CSV (SRI_Presion_Fiscal.csv).

**Razonamiento**:
Aunque en este caso conocemos la URL directa del archivo CSV por interacciones previas, en un proceso ETL real, se analizaría el HTML obtenido para localizar dinámicamente el enlace de descarga basándose en patrones (nombre del archivo, extensión, atributos del enlace). Usaremos la URL directa para la descarga en el siguiente paso por eficiencia.

### Subtarea 1.3: Descargar el archivo CSV

Descargar el archivo CSV de Presión Fiscal utilizando su URL directa.

**Razonamiento**:
Dado que ya conocemos la URL exacta del archivo CSV, utilizamos la biblioteca `requests` para descargarlo directamente al entorno de Colab.
"""

import requests
import os

# URL directa del archivo CSV de Presión Fiscal
csv_url = "https://www.sri.gob.ec/o/sri-portlet-biblioteca-alfresco-internet/descargar/7e45627e-1f7e-4e21-ae59-d520634fc63f/SRI_Presion_Fiscal.csv"
file_path = "SRI_Presion_Fiscal.csv"

try:
    print(f"Intentando descargar el archivo desde: {csv_url}")
    response = requests.get(csv_url)
    response.raise_for_status()  # Lanzar un error HTTP para respuestas de error (4xx o 5xx)

    # Escribir el contenido del archivo en un archivo local
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"Archivo descargado con éxito a: {file_path}")

except requests.exceptions.RequestException as e:
    print(f"Error al descargar el archivo: {e}")

"""## 2. Transformación

La fase de Transformación se encarga de limpiar, validar y estructurar los datos extraídos para que sean adecuados para el destino (Google Sheets).

### Subtarea 2.1: Instalar bibliotecas necesarias

Instalar las bibliotecas `pandas` para leer el archivo CSV y `gspread` y `google-auth` para interactuar con Google Sheets.

**Razonamiento**:
Instalamos las bibliotecas requeridas utilizando pip. `pandas` es necesaria para la manipulación de datos, y `gspread` y `google-auth` son esenciales para interactuar con Google Sheets.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install pandas gspread google-auth

"""### Subtarea 2.2: Leer el archivo CSV en un DataFrame

Cargar los datos del archivo CSV descargado en un DataFrame de pandas, especificando la codificación y el delimitador correctos.

**Razonamiento**:
Utilizamos la biblioteca `pandas` para leer el archivo CSV. Es crucial especificar la codificación ('latin1') y el delimitador (';') que identificamos previamente para que los datos se lean correctamente en columnas. Mostramos las primeras filas para verificar la lectura.
"""

import pandas as pd

file_path = "SRI_Presion_Fiscal.csv"

try:
    # Leer el archivo CSV con la codificación y delimitador correctos
    df = pd.read_csv(file_path, encoding='latin1', sep=';')
    print(f"Archivo {file_path} leído con éxito en un DataFrame.")
    display(df.head())
except FileNotFoundError:
    print(f"Error: El archivo {file_path} no fue encontrado.")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo CSV: {e}")

"""### Subtarea 2.3: Limpiar y transformar los datos

Realizar las transformaciones necesarias en el DataFrame, como convertir la columna de porcentaje a numérico.

**Razonamiento**:
Convertimos la columna ' %_Presion ' a tipo numérico. Esto implica reemplazar el separador decimal (coma) por un punto y luego convertir la columna. También manejamos los espacios en el nombre de la columna.
"""

import pandas as pd

try:
    # Limpiar espacios en los nombres de las columnas
    df.columns = df.columns.str.strip()
    print("Espacios iniciales/finales eliminados de los nombres de las columnas.")
    print("Nombres de columnas actualizados:", df.columns.tolist())

    # Reemplazar coma por punto en la columna '%_Presion' y convertir a numérico
    # Asegurarnos de que la columna '%_Presion' exista después de limpiar los nombres
    if '%_Presion' in df.columns:
        df['%_Presion'] = df['%_Presion'].astype(str).str.replace(',', '.', regex=False)
        df['%_Presion'] = pd.to_numeric(df['%_Presion'], errors='coerce')
        print("Columna '%_Presion' convertida a tipo numérico exitosamente.")
        display(df.head())
        display(df.info())
    else:
        print("Error: La columna '%_Presion' no fue encontrada después de limpiar los nombres.")


except KeyError:
    print("Error: Una columna esperada no fue encontrada durante la transformación.")
except Exception as e:
    print(f"Ocurrió un error durante la limpieza y transformación de los datos: {e}")

"""## 3. Carga

La fase de Carga se encarga de mover los datos transformados al sistema de destino, en este caso, una hoja de Google Sheets.

### Subtarea 3.1: Autenticar con Google Sheets

Configurar la autenticación para permitir el acceso a Google Sheets.

**Razonamiento**:
Autenticamos con Google usando `google.colab.auth` para permitir el acceso a Google Drive y Google Sheets. Esto requerirá interacción del usuario para otorgar permisos.
"""

from google.colab import auth
auth.authenticate_user()

"""### Subtarea 3.2: Conectarse a la hoja de cálculo de Google Sheets

Abrir la hoja de cálculo "Práctica ETL" en Google Sheets.

**Razonamiento**:
Usamos la biblioteca `gspread` y las credenciales autenticadas para abrir la hoja de cálculo especificada por su título.
"""

import gspread
from google.colab import auth
from google.auth import default

# Authenticate and create the gspread client
# Assuming authentication has been done in a previous step (388e0b57)
try:
    creds, _ = default()
    gc = gspread.authorize(creds)

    # Open the spreadsheet by title
    spreadsheet_name = "Práctica ETL"
    sh = gc.open(spreadsheet_name)

    print(f"Conectado exitosamente a la hoja de cálculo: {spreadsheet_name}")

except gspread.SpreadsheetNotFound:
    print(f"Error: La hoja de cálculo '{spreadsheet_name}' no fue encontrada.")
except Exception as e:
    print(f"Ocurrió un error al conectar con Google Sheets: {e}")

"""### Subtarea 3.3: Seleccionar la hoja de trabajo

Acceder a la hoja específica llamada "DataSet" dentro de la hoja de cálculo.

**Razonamiento**:
Usamos el método `worksheet()` del objeto de la hoja de cálculo para seleccionar la hoja con el nombre "DataSet".
"""

try:
    # Select the worksheet by name
    worksheet_name = "DataSet"
    worksheet = sh.worksheet(worksheet_name)

    print(f"Hoja de trabajo '{worksheet_name}' seleccionada exitosamente.")

except gspread.WorksheetNotFound:
    print(f"Error: La hoja de trabajo '{worksheet_name}' no fue encontrada en la hoja de cálculo.")
except Exception as e:
    print(f"Ocurrió un error al seleccionar la hoja de trabajo: {e}")

"""### Subtarea 3.4: Limpiar la hoja de trabajo existente

Borrar el contenido actual de la hoja "DataSet".

**Razonamiento**:
Usamos el método `clear()` del objeto de la hoja de trabajo para eliminar todos los datos existentes de la hoja antes de escribir los nuevos datos.
"""

try:
    worksheet.clear()
    print(f"Contenido de la hoja de trabajo '{worksheet_name}' limpiado exitosamente.")

except Exception as e:
    print(f"Ocurrió un error al limpiar la hoja de trabajo: {e}")

"""### Subtarea 3.5: Escribir los datos transformados en la hoja de trabajo

Cargar los datos del DataFrame de pandas (con las transformaciones aplicadas) en la hoja "DataSet".

**Razonamiento**:
Convertimos el DataFrame de pandas a una lista de listas, incluyendo los encabezados, y usamos el método `update()` del objeto de la hoja de trabajo para escribir los datos en la hoja.
"""

try:
    # Convert the DataFrame to a list of lists, including the header
    data_to_upload = [df.columns.values.tolist()] + df.values.tolist()

    # Write the data to the worksheet
    worksheet.update(data_to_upload)

    print("Datos del DataFrame transformado cargados exitosamente en la hoja de trabajo.")

except Exception as e:
    print(f"Ocurrió un error al escribir los datos transformados en la hoja de trabajo: {e}")