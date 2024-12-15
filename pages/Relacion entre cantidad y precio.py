import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurar la ruta de la base de datos
db_path = r"C:\Users\Saray\Downloads\progra\proyecto\Northwind_small.sqlite"

# Título de la aplicación
st.title("Relación entre el Precio y la Cantidad Comprada")

# Objetivo del gráfico
st.markdown(
    """
    Este gráfico de dispersión tiene como objetivo analizar si existe una relación entre el precio de los productos y la cantidad comprada. 
    Podremos observar si los productos más caros tienden a tener menor demanda.
    """
)

# Lista de ciudades de América
ciudades_america = [
    'Buenos Aires', 'Caracas', 'México D.F.', 'São Paulo', 'Rio de Janeiro',
    'Montréal', 'Vancouver', 'Portland', 'San Francisco', 'Seattle', 'San Cristóbal', 'Resende'
]

# Selección de ciudad en Streamlit
ciudad_seleccionada = st.selectbox("Seleccione una ciudad:", ciudades_america)

# Conexión a la base de datos y extracción de datos
try:
    conn = sqlite3.connect(db_path)
    query = f'''
        SELECT od.UnitPrice, od.Quantity
        FROM OrderDetail od
        JOIN Product p ON od.ProductID = p.Id
        JOIN [Order] o ON od.OrderID = o.Id
        JOIN Customer c ON o.CustomerID = c.Id
        WHERE c.City = "{ciudad_seleccionada}"
    '''
    df = pd.read_sql_query(query, conn)


    if df.empty:
        st.warning("No se encontraron datos para la ciudad seleccionada.")
    else:
        # Crear el gráfico de dispersión
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='UnitPrice', y='Quantity', data=df, color='blue', ax=ax)
        ax.set_title(f'Relación entre el Precio y la Cantidad Comprada - {ciudad_seleccionada}')
        ax.set_xlabel('Precio del Producto (UnitPrice)')
        ax.set_ylabel('Cantidad Comprada (Quantity)')

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")

finally:
    conn.close()