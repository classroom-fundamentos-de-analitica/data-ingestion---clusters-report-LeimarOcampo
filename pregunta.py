"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd
import re

def ingest_data():
    df = open('clusters_report.txt', 'r')
    lineASIE = re.sub("\s{3,}", "  ", df.readline().strip()).split("  ")
    lineMiravo = df.readline().replace("\n", "").strip().split("  ")
    for i in range(len(lineASIE)):
      lineASIE[i] = (lineASIE[i].strip().lower()).replace(" ", "_")
      if i == 1 or i == 2:
        lineASIE[i] = (lineASIE[i] + ' ' + lineMiravo[i-1].lower()).replace(" ", "_")
    df.readline(), df.readline()
    documento = df.readlines()
    content = []
    texto = ''
    for line in documento:
      line = re.sub(r"\s{2,}", " ", line.strip()).replace('\n', '')
      line += ' '
      if '%' in line:
        if texto != '': 
          aux = content.pop()
          texto = texto.replace('.', '').strip()
          aux[3] = aux[3] + texto
          content.append(aux)
          texto = ''
        indice = line.index('%')
        sublista = line[:indice].strip().replace(',', '.').split(" ")
        content.append(sublista + [line[indice + 2:]])
      else:
        texto += line
    aux = content.pop()
    texto = texto.replace('.', '').strip()
    aux[3] = aux[3] + texto
    content.append(aux)
    dataframe = pd.DataFrame(content, columns = lineASIE)
    dataframe['cluster'] = dataframe['cluster'].astype('int64')
    dataframe['cantidad_de_palabras_clave'] = dataframe['cantidad_de_palabras_clave'].astype('int64')
    dataframe['porcentaje_de_palabras_clave'] = dataframe['porcentaje_de_palabras_clave'].astype('float64')
    
    return dataframe