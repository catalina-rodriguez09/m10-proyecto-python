import os
import pandas as pd
from thefuzz import fuzz, process

# DEFINIR EL DIRECTORIO DE TRABAJO(LUGAR EN EL CUAL SE ENCUENTRAN LOS ARCHIVOS)

directorio = r"C:\Users\Catalinas\Desktop\CURSO ANALISIS DE DATOS\MODULO 10\proyecto"

os.chdir(directorio)

#print("Directorio de trabajo", os.getcwd())

df_ventas = pd.read_csv("Ventas.csv")

df_vendedores = pd.read_csv("Vendedores.csv")

#print(df_ventas.info())

#print(df_vendedores.info())

#limpiar nombres de empresas

df_ventas["empresa"] = df_ventas["empresa"].str.lower().str.strip()
df_vendedores["empresa"] = df_vendedores["empresa"].str.lower().str.strip()

#para borrar caracteres como linea guion etc)

#print(df_ventas["empresa"])

def encontrar_mejor_match(nombre, lista_empresas):
    mejor_match, score = process.extractOne(nombre, lista_empresas, scorer=fuzz.token_sort_ratio)

    print(score)
    return mejor_match if score > 50 else None

df_ventas["empresa_corregida"] = df_ventas["empresa"].apply(lambda x : encontrar_mejor_match(x, df_vendedores["empresa"].tolist()))


#print(df_ventas.tail(10))

df_final = df_ventas.merge(df_vendedores, left_on="empresa_corregida", right_on="empresa", how="left")
#drop(columns=["empresa_y"])

# corregir nombres de las columnas

df_final.rename(columns={"empresa_x": "empresa_original"}, inplace=True)

#print(df_final.head())

df_sin_match = df_final[df_final["empresa_corregida"].isna()]

print(df_sin_match.head())

#guardar los reportes de los 2 dataframes

df_final.to_csv("resultado_cruce.csv", index=False)

df_sin_match.to_csv("resultado_sin_cruce.csv", index=False)
