# Libraries:
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import datetime
import folium
from streamlit_folium import folium_static
from PIL import Image
from haversine import haversine
import numpy as np
import matplotlib
matplotlib.use('agg')
st.set_page_config(page_title="Restaurant's Overview", page_icon='🍽️', layout='wide')


# =============================
# Functions
# =============================


def avg_std_time_on_traffic(df1):
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = (df1.loc[:, cols]
              .groupby(['City', 'Road_traffic_density'])
              .agg({'Time_taken(min)': ['mean', 'std']}))
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time',
                      color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig


def avg_std_time_chart(df1):
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']}).round(0)
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'],
                         error_y=dict(type='data', array=df_aux['std_time']),
                         marker_color='lightblue'))
    fig.update_traces(text=df_aux['avg_time'], textposition='auto', textfont=dict(size=14))
    fig.update_layout(barmode='group')
    return fig


def avg_std_time_delivery(df1, op, festival):
    """
        This function calculates the mean time and standard deviation for delivery time.

        Parameters:
            df (DataFrame): The dataframe containing the necessary data for the calculation.
            op (str): The type of operation, either 'avg_time' or 'std_time'.
            festival (str): 'Yes' or 'No'
        Returns:
            DataFrame: A dataframe with two columns and one row, containing the calculated results.
    """

    df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
              .groupby('Festival')
              .agg({'Time_taken(min)': ['mean', 'std']}))

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)
    return df_aux


def distance(df1, fig):
    if not fig:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude',
                'Delivery_location_longitude']

        df1['distance'] = df1.loc[:, cols].apply(lambda x:
                                                 haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                           (x['Delivery_location_latitude'],
                                                            x['Delivery_location_longitude'])), axis=1)
        avg = np.round(df1['distance'].mean(), 2)

        return avg
    else:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude',
                'Delivery_location_longitude']

        df1['distance'] = df1.loc[:, cols].apply(lambda x:
                                                 haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                           (x['Delivery_location_latitude'],
                                                            x['Delivery_location_longitude'])), axis=1)
        avg = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index().round(0)
        fig = go.Figure(data=[go.Pie(labels=avg['City'], values=avg['distance'], pull=[0, 0.1, 0])])
        return fig


def clean_code(df1):
    # Function to clean dataframe: removing "NaN", fixing data types, removing spaces within strings/text/object,
    # formatting Data column, separating text from int column, remove 'condition' word
    # Input: Dataframe and Output: Dataframe

    selected_lines = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[selected_lines, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    selected_lines = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[selected_lines, :].copy()

    selected_lines = df1['City'] != 'NaN '
    df1 = df1.loc[selected_lines, :].copy()

    selected_lines = df1['Festival'] != 'NaN '
    df1 = df1.loc[selected_lines, :].copy()

    selected_lines = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[selected_lines, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # First, we need to reset the index of the dataset, because the NaN lines exclusion.
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # Cleaning Time_taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    # Cleaning Weatherconditions:
    df1['Weatherconditions'] = df1['Weatherconditions'].apply(lambda x: x.split('conditions ')[1])

    return df1


# =============================
# Code Logic
# =============================
# Import dataset:
df = pd.read_csv('dataset/train.csv')
df1 = clean_code(df)

# =============================
# Sidebar
# =============================
st.header("Marketplace - Restaurant's Overview")

image = Image.open('logo.jpg')
st.sidebar.image(image, use_column_width=True)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")

st.sidebar.markdown("##### Select a date:")
date_slider = st.sidebar.slider('What is the cutoff date you wish to consider?',
                                value=datetime.datetime(2022, 4, 13),
                                min_value=datetime.datetime(2022, 2, 11),
                                max_value=datetime.datetime(2022, 4, 6),
                                format='DD-MM-YYYY')

st.sidebar.markdown("""---""")
st.sidebar.markdown("##### Select traffic conditions:")
traffic_options = st.sidebar.multiselect(" ",
                                         ['Low', 'Medium', 'High', 'Jam'],
                                         default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
weather_conditions = st.sidebar.multiselect('Select weather conditions: ',
                                            ['Cloudy', 'Fog', 'Sandstorms', 'Stormy', 'Sunny', 'Windy'],
                                            default=['Cloudy', 'Fog', 'Sandstorms', 'Stormy', 'Sunny', 'Windy'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('#### Powered by DS Community')

# Data selection
selected_lines = df1['Order_Date'] < date_slider
df1 = df1.loc[selected_lines, :]

# Traffic selection
selected_lines = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[selected_lines, :]

# Weather selection
selected_lines = df1['Weatherconditions'].isin(weather_conditions)
df1 = df1.loc[selected_lines, :]

# =============================
# Layout
# =============================
tab1= st.tabs(['Manager View'])

with st.container():
    st.title('Overall Restaurants Metrics')
    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
        col1.metric('Number of Delivery drivers', delivery_unique)
        avg = distance(df1, fig=False)
        st.metric('Avg distance between restaurants and delivery locations:', avg)

    with col2:
        df_aux = avg_std_time_delivery(df1, 'avg_time', festival='Yes')
        col2.metric('Avg delivery time with Festival:', df_aux)
        df_aux = avg_std_time_delivery(df1, 'std_time', festival='Yes')
        st.metric('Standard deviation time with Festival:', df_aux)

    with col3:
        df_aux = avg_std_time_delivery(df1, 'avg_time', festival='No')
        col3.metric('Average delivery time without Festival:', df_aux)
        df_aux = avg_std_time_delivery(df1, 'std_time', festival='No')
        st.metric('Standard deviation time without Festival:', df_aux)



with st.container():
    st.markdown("""___""")
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.title("Average delivery time (min) by city")
        fig = avg_std_time_chart(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.title("Average and standard deviation of delivery times (min) by city and type of order")
        cols = ['City', 'Time_taken(min)', 'Type_of_order']
        df_aux = (df1.loc[:, cols]
                  .rename(columns={'Type_of_order': 'Type of Order'})
                  .groupby(['City', 'Type of Order'])
                  .agg({'Time_taken(min)': ['mean', 'std']})
                  .round(2))

        df_aux.columns = ['Avg Time', 'Std Time']

        df_aux = df_aux.reset_index()
        df_aux_styled = df_aux.style.background_gradient(cmap='Blues').format(
            {'Avg Time': '{:.2f}', 'Std Time': '{:.2f}'})

        st.dataframe(df_aux_styled, hide_index=True)
with st.container():
    st.markdown("""___""")
    st.title("Delivery Speed Analysis")

    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown(
            'When considering the average of all the delivery distances from various cities together, the portion corresponding to each city is:')
        fig = distance(df1, fig=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('Sunburst chart (compass rose) to visualize the average and standard deviation of delivery time in different cities and traffic densities:')
        fig = avg_std_time_on_traffic(df1)
        st.plotly_chart(fig, use_container_width=True)
