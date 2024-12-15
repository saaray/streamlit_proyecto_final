# Importar las bibliotecas necesarias
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Ruta completa de la base de datos
db_path = r"C:\Users\Saray\Downloads\progra\proyecto\Northwind_small.sqlite"

# Título en Streamlit
st.title("Clientes por Ciudad en América")

# Objetivo del gráfico
st.write("""
El siguiente gráfico muestra la cantidad de clientes en distintas ciudades de América, permitiendo analizar la distribución geográfica de los clientes en ciudades clave. 
Este análisis es útil para identificar áreas con mayor concentración de clientes y orientar esfuerzos de marketing o expansión.
""")

# Lista de ciudades de América que deseas incluir en el gráfico
cities_america = [
    'Buenos Aires', 'Caracas', 'México D.F.', 'São Paulo', 'Rio de Janeiro',
    'Montréal', 'Vancouver', 'Portland', 'San Francisco', 'Seattle', 'San Cristóbal', 'Resende'
]

# Conectar a la base de datos y consultar los datos
try:
    conn = sqlite3.connect(db_path)

    query = f'''
    SELECT City, COUNT(Id) as Num_Customers
    FROM Customer
    WHERE City IN ({", ".join([f"'{city}'" for city in cities_america])})
    GROUP BY City
    ORDER BY Num_Customers DESC
    '''

    # Ejecutar la consulta y cargar los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Num_Customers', y='City', data=df, palette='viridis')

    # Añadir títulos y etiquetas
    plt.title('Cantidad de Clientes por Ciudad en América')
    plt.xlabel('Número de Clientes')
    plt.ylabel('Ciudad')

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

except Exception as e:
    st.write(f"Error al ejecutar la consulta: {e}")
