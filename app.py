import pandas as pd
import streamlit as st
import plotly.express as px 

# Leer los datos
car_data = pd.read_csv('vehicles_us.csv') 

# Título de la aplicación
st.header('Análisis de Vehículos Usados en EE. UU.')

# Descripción breve
st.write("Seleccione una casilla de verificación para mostrar el gráfico correspondiente.")

# Casilla de verificación para el histograma de precios
if st.checkbox('Mostrar Histograma de Precios'):
    # Crear el histograma usando plotly-express
    fig_price = px.histogram(car_data, x='price', nbins=50, title='Distribución de Precios de Vehículos')
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_price)

# Casilla de verificación para el gráfico de dispersión de precio vs. odómetro
if st.checkbox('Mostrar Gráfico de Dispersión de Precio vs. Odómetro'):
    # Crear el gráfico de dispersión
    fig_price_odometer = px.scatter(car_data, x='odometer', y='price', color='condition',
                                    title='Precio vs. Odómetro por Condición del Vehículo')
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_price_odometer)

# Casilla de verificación para el diagrama de caja de precios por tipo
if st.checkbox('Mostrar Diagrama de Caja de Precios por Tipo de Vehículo'):
    # Crear el diagrama de caja
    fig_price_type = px.box(car_data, x='type', y='price', color='type', 
                            title='Precios de Vehículos por Tipo')
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_price_type)

# Casilla de verificación para el gráfico de barras de vehículos por tipo de combustible
if st.checkbox('Mostrar Gráfico de Barras por Tipo de Combustible'):
    # Crear el gráfico de barras
    fig_fuel = px.bar(car_data, x='fuel', title='Número de Vehículos por Tipo de Combustible')
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_fuel)

# Casilla de verificación para el gráfico de líneas del precio promedio a lo largo del tiempo
if st.checkbox('Mostrar Gráfico de Líneas del Precio Promedio a lo Largo del Tiempo'):
    # Crear el gráfico de líneas
    car_data['date_posted'] = pd.to_datetime(car_data['date_posted'])
    df_avg_price = car_data.groupby('date_posted')['price'].mean().reset_index()
    fig_avg_price = px.line(df_avg_price, x='date_posted', y='price', 
                            title='Precio Promedio del Vehículo a lo Largo del Tiempo')
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_avg_price)

# Casilla de verificación para el gráfico de los 10 modelos más populares por marca
if st.checkbox('Mostrar Gráfico de Modelos Más Populares por Marca'):
    # Filtrar los 10 modelos más populares por marca
    popular_models = car_data.groupby(['model'])['model'].count().nlargest(10)

    # Crear un gráfico de barras apiladas para mostrar los modelos más populares por marca
    fig_popular_models = px.bar(car_data[car_data['model'].isin(popular_models.index)], x='model', color='model', 
                                title='Top 10 Modelos Más Populares por Marca',
                                labels={'model': 'Modelo', 'count': 'Cantidad'})
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_popular_models)


brands = car_data['model'].apply(lambda x: x.split(' ')[0]).unique()

# Seleccionar una marca de autos
selected_brand = st.selectbox('Selecciona una marca de autos:', brands)

# Filtrar los datos para la marca seleccionada y obtener los 5 modelos más vendidos
filtered_data = car_data[car_data['model'].str.startswith(selected_brand)]
top_models = filtered_data['model'].value_counts().nlargest(5).index
top_models_data = filtered_data[filtered_data['model'].isin(top_models)]

# Crear un gráfico de barras apiladas para mostrar los 5 modelos más vendidos de la marca seleccionada
fig = px.bar(top_models_data, x='model', color='model', 
             title=f'Top 5 Modelos Más Vendidos de {selected_brand}',
             labels={'model': 'Modelo', 'count': 'Cantidad'})

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)