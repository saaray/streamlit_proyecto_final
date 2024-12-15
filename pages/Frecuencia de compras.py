import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurar la ruta de la base de datos
db_path = r"C:\Users\Saray\Downloads\progra\proyecto\Northwind_small.sqlite"

# Título de la aplicación
st.title("Frecuencia de Compras por Cliente")

# Objetivo del gráfico
st.markdown(
    """
    Este histograma tiene como objetivo analizar la frecuencia de compras de los clientes. 
    Podremos observar si hay clientes frecuentes o si la mayoría compra de manera esporádica.
    """
)

# Conexión a la base de datos y extracción de datos
try:
    conn = sqlite3.connect(db_path)
    query = '''
        SELECT c.Id AS CustomerID, COUNT(o.Id) AS PurchaseFrequency
        FROM [Order] o
        JOIN Customer c ON o.CustomerID = c.Id
        GROUP BY c.Id
    '''
    df = pd.read_sql_query(query, conn)

    if df.empty:
        st.warning("No se encontraron datos.")
    else:
        # Crear el histograma
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df['PurchaseFrequency'], bins=10, kde=False, color='blue', ax=ax)
        ax.set_title('Frecuencia de Compras por Cliente')
        ax.set_xlabel('Frecuencia de Compras')
        ax.set_ylabel('Número de Clientes')

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")

finally:
    conn.close()
