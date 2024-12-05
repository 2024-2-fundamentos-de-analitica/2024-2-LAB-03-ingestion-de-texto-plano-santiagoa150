"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import glob
import fileinput
import pandas as pd


def load_data(input_file: str):
    file = glob.glob(input_file)
    lines = []
    with fileinput.input(files=file) as f:
        for line_number, line in enumerate(f, start=1):
          if line_number > 4:
            lines.append(line.strip()) 
    return lines 

def clean_data(lines):
    processed = []

    cluster = None
    cantidad = None
    porcentaje = None
    palabras_clave = []
    
    for line in lines:
      line = line.strip()
      if line == "":
        continue

      if line.split()[0].isdigit():
        if cluster is not None:
          processed.append([cluster, cantidad, porcentaje, " ".join(palabras_clave)])
        # Procesa la nueva línea
        partes = line.split(maxsplit=4)
        cluster = int(partes[0])
        cantidad = int(partes[1])
        porcentaje = float(partes[2].replace(",", "."))
        palabras_clave = [partes[4]]
      else:
        palabras_clave.append(line)

    if cluster is not None:
      processed.append([cluster, cantidad, porcentaje, " ".join(palabras_clave)])

    return processed

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    lines = load_data('files/input/clusters_report.txt')
    data = clean_data(lines)
    df = pd.DataFrame(data, columns=['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'])
    df['principales_palabras_clave'] = df['principales_palabras_clave'].apply(lambda x: x.split(','))
    df['principales_palabras_clave'] = df['principales_palabras_clave'].apply(lambda x: ', '.join([' '.join(word.replace('.', '').split()) for word in x]))
    return df
