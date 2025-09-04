#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:40:56 2024

@author: emmettdiez
"""
#%%

# Para realizar esta actividad he creado un entorno en el terminal de mi ordenador con "canda create" y posteriormente fue activado "canda activate" e instalé las librerías necesarias con "conda install" (Spyder, Pandas, Seaborn...).
# En primer lugar cargo las librerías necesarias para la actividad.
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt

#%%
# A continuación abro el archivo con la secuencia y filtro por SEQRES utilizando.
# Utilizo los condicionales IF y ELIF para acotar las posiciones y filas que contienen información de aminoácidos.

seqres = []

with open("/Users/emmettdiez/1tup.pdb", mode = 'r') as file:
    for linea in file:
        resultado = re.search(r'^SEQRES', linea)
        if resultado:
            lista = linea.split()
            if len(lista) == 17:
                seqres.append(lista[-13:])
            elif len(lista) == 15:
                seqres.append(lista[-11:])
            
print(seqres)

# Con esta instrucción elimino las dos primeras linas ya que no contienen secuencias de aminoácidos.
seqres = seqres[2:]

# Utilizo el LIST COMPREHENSION para aplanar la lista con sublistas de aminoacidos. 
seqres = [aminoacido for lista in seqres for aminoacido in lista]
print(seqres)

# Finalmente creo el diccionario para contar las veces que aparece cada aminoácido:

dicc_seqres = {aminoacido: seqres.count(aminoacido) for aminoacido in seqres}

print(dicc_seqres)
#%%

# Por útlimo, hago el Histograma con Seaborn. Para etsto necesito crear un dataframe con pandas porque no es capaz de leer el diccionario. 

df = pd.DataFrame(list(dicc_seqres.items()), columns=['Aminoacidos', 'Frecuencia'])

# Crear el histograma usando Seaborn
sns.histplot(data=df, x='Aminoacidos', weights='Frecuencia', discrete=True, color="purple")
plt.title("Frecuencia de aminoacidos en SEQRES", fontsize=16, color="red")
plt.xlabel("Aminoacidos", fontsize=12, color="green")
plt.ylabel("Frecuencias", fontsize=12, color="blue")
plt.xticks(rotation=90)
# Mostrar el gráfico
plt.show()

#%%

# Importo el archivo CSV con las ciudades y cambio el nombre de las columnas:
    
data = pd.read_csv("/Users/emmettdiez/Actividad1/actividad.csv", sep= ';')

data = data.rename(columns={"id": "id", "diet": "dieta", "pulse": "pulsaciones", "time": "tiempo", "kind": "actividad"})

data.columns # Compruebo que se ha cambiado el nombre de las columnas

# Identifico los valores faltantes, aunque en este caso no hay:

print(data.isnull().sum())

# Con value_counts() averiguo los niveles dentro de la columna dieta, que son dos (low fat/ no fat) y sus frecuencias:

niveles_dieta = data['dieta'].value_counts()

# Utilizo Groupby para agrupar los datos por nivel de actividad:

grupo = data.groupby('actividad').size()

# Con la funcion ZIP extraemos de cada lista la combinación ( en formato tuplas) de cada estado de actividad y su frecuencia. 

actividades = [x for x in zip(grupo.index.tolist(), [x for x in grupo])]


# Calculamos frecuencia cardiaca media y desviacion estandar para cada actividad con ayuda del argumento .agg:

grupo = data.groupby('actividad')

frecuencia_cardiaca = grupo['pulsaciones'].agg(["mean", "std"])

print(frecuencia_cardiaca)

# Usamos la funcion merge para unuir las ciudades de ecada paciente a sus id.
# Creo un dataframe al importar el archivo .tsv para poder hacer el merge después, porque es preciso que se haga entre dos dataframes.
df_ciudades = pd.read_csv("/Users/emmettdiez/Actividad1/ciudades.tsv", sep = '\t', header = None, names = ['id', 'city'])

data['id'] = data['id'].astype(str) # Con esta linea igualo los formatos de las columnas que contienen el ID, lo cual es necesario para el merge.

df_comun = pd.merge(left=data, right=df_ciudades, on="id") # Este es el dataframe común con las ciudades asociadas. 

# Contsruimos el gráfico con las librerias seaborn donde la ufncion FacetGrid nos muestra una unica grafica por facetas.

grafico = sns.FacetGrid(data, col="actividad", row="dieta", margin_titles=True, height=4)
grafico.map(sns.scatterplot, "tiempo", "pulsaciones",color = "b")

# Ajustamos los ejes y el titulo:
grafico.set_axis_labels("Tiempo (min)", "Pulsaciones (bpm)")
grafico.set_titles(col_template="{col_name}", row_template="{row_name}")
plt.subplots_adjust(top=1.0)
grafico.fig.suptitle("Relación de las pulsaciones y el tiempo en función de la dieta y actividad")

# Ajustamos tamaño de la figura y los títulos:
plt.figure(figsize=(10, 8))
plt.subplots_adjust(top=0.9)
grafico.fig.suptitle('Relación de las pulsaciones y el tiempo en función de la dieta y actividad', fontsize=16)
grafico.set_axis_labels("Tiempo (min)", "Pulsaciones (bpm)")

plt.show()




























