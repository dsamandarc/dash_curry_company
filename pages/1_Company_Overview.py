# Libraries:
import plotly.express as px
import pandas as pd
import streamlit as st
import datetime
import folium
from streamlit_folium import folium_static
from PIL import Image

st.set_page_config(page_title='Company  Overview', page_icon='📈', layout='wide')
# =============================
# Functions
# =============================
def country_maps(df1):
    # Central location of each city by traffic type.
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = (df1.loc[:, cols]
              .groupby(['City', 'Road_traffic_density'])
              .median()
              .reset_index())

    # Draw the map
    map1 = folium.Map()

    # Marker receives a list of latitude and longitude, and we add to the map created with add_to.
    for index, location_info in df_aux.iterrows():
        (folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']]).add_to(map1))
    folium_static(map1, width=1024, height=600)

def orders_by_week_person(df1):
    # Orders volume by week of the year.
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                .groupby('week_of_year')
                .nunique()
                .reset_index())
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
    return fig


def orders_by_week(df1):
    # In my dataset I don't have the week of the year column, so I need to create using %U(Sunday as first day of the
    # week, %W is monday the first day of the week). But first I need to transform my df1['Order_Date'] that is a
    # Series in a Data type.
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = (df1.loc[:, ['ID', 'week_of_year']]
              .groupby('week_of_year')
              .count()
              .reset_index())

    # Line chart - using Plotly
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig


def orders_by_city_traffic(df1):
    # Comparison of order volumes by city and traffic type.
    df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
              .groupby(['City', 'Road_traffic_density'])
              .count()
              .reset_index())
    # Scatter plot
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig


def orders_by_traffic(df1):
    # Distribution of orders by type of traffic.
    df_aux = (df1.loc[:, ['ID', 'Road_traffic_density']]
              .groupby('Road_traffic_density')
              .count()
              .reset_index())
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    df_aux['deliveries_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    # Pie chart

    fig = px.pie(df_aux, values='deliveries_perc', names='Road_traffic_density')
    return fig


def order_metric(df1):
    # Distribution of orders in timeline.
    # Select columns
    cols = ['ID', 'Order_Date']
    # Select lines
    df_aux = (df1.loc[:, cols]
              .groupby('Order_Date')
              .count()
              .reset_index())
    # Chart
    fig = px.bar(df_aux, x='Order_Date', y='ID')
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
st.header('Marketplace - Company Overview')

image = Image.open('logo.jpg')
st.sidebar.image(image, use_column_width=True)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")

st.sidebar.markdown("## Select a date:")
date_slider = st.sidebar.slider('What is the cutoff date you wish to consider?',
                                value=datetime.datetime(2022, 4, 13),
                                min_value=datetime.datetime(2022, 2, 11),
                                max_value=datetime.datetime(2022, 4, 6),
                                format='DD-MM-YYYY')

st.sidebar.markdown("""---""")
traffic_options = st.sidebar.multiselect('Select traffic conditions: ',
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
tab1, tab2, tab3 = st.tabs(['Manager View', 'Strategic View', 'Geographical View'])
with tab1:
    with st.container():
        # Number of orders per day.
        st.markdown('### Daily Order Count')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Orders by Traffic Type')
            fig = orders_by_traffic(df1)
            st.plotly_chart(fig, use_container_width=True, )

        with col2:
            st.markdown('### Order Volume: City and Traffic Comparison')
            fig = orders_by_city_traffic(df1)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
        # Number of orders per week.
        st.markdown('### Weekly Order Summary')
        fig = orders_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        # Number of orders per delivery person per week.
        st.markdown('### Weekly Deliveries per Delivery Person')
        fig = orders_by_week_person(df1)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown('### City Traffic Distribution')
    country_maps(df1)
