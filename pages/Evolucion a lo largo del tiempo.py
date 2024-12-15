import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Configurar la ruta de la base de datos
db_path = r"C:\Users\Saray\Downloads\progra\proyecto\Northwind_small.sqlite"

# Título de la aplicación
st.title("Evolución de Nuevos Clientes a lo Largo del Tiempo")

# Objetivo del gráfico
st.markdown(
    """
    Este gráfico de líneas muestra la evolución de la cantidad de clientes nuevos a lo largo del tiempo. 
    Es útil para identificar tendencias estacionales o anuales en la adquisición de clientes 
    y evaluar la efectividad de las campañas de marketing.
    """
)

# Conexión a la base de datos y extracción de los datos para el filtro de años
try:
    conn = sqlite3.connect(db_path)
    # Consultamos los años disponibles en los pedidos
    year_query = '''
        SELECT DISTINCT strftime('%Y', OrderDate) AS Year
        FROM "Order"
        ORDER BY Year
    '''
    years_df = pd.read_sql_query(year_query, conn)

    if years_df.empty:
        st.warning("No se encontraron datos de años.")
    else:
        # Agregar un filtro de selección de año
        selected_year = st.selectbox("Selecciona el Año:", years_df['Year'].tolist())

        # Ahora que tenemos el año seleccionado, creamos la consulta para los nuevos clientes en ese año
        query = f'''
            SELECT strftime('%Y-%m', OrderDate) AS Month, COUNT(DISTINCT CustomerId) AS NewCustomers
            FROM "Order"
            WHERE strftime('%Y', OrderDate) = '{selected_year}'
            GROUP BY Month
            ORDER BY Month
        '''
        df = pd.read_sql_query(query, conn)

        if df.empty:
            st.warning(f"No se encontraron datos para el año {selected_year}.")
        else:
            # Crear el gráfico de líneas
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['Month'], df['NewCustomers'], marker='o', color='blue')
            ax.set_title(f'Evolución de Nuevos Clientes en {selected_year}')
            ax.set_xlabel('Mes')
            ax.set_ylabel('Cantidad de Nuevos Clientes')
            plt.xticks(rotation=45)

            # Mostrar el gráfico en Streamlit
            st.pyplot(fig)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")

finally:
    conn.close()
