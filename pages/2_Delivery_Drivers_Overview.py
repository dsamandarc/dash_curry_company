# Libraries:
import pandas as pd
import streamlit as st
import datetime
from PIL import Image



st.set_page_config(page_title='Delivery Drivers Overview', page_icon='🛵', layout='wide')

# =============================
# Functions
# =============================


def top_delivers(df1, top_asc):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
           .rename(columns={'Time_taken(min)': 'Time Taken (min)', 'Delivery_person_ID': 'Delivery Person ID'})
           .groupby(['City', 'Delivery Person ID'])
           .mean()
           .sort_values(['City', 'Time Taken (min)'], ascending=top_asc)
           .reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3

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
st.header('Marketplace - Delivery Drivers Performance Overview')

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
tab1 = st.tabs(['Manager View'])

with st.container():
    st.title('Overall Performance Metrics')
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
        oldest = df1.loc[:, 'Delivery_person_Age'].max()
        col1.metric('Oldest:', oldest)
    with col2:
        youngest = df1.loc[:, 'Delivery_person_Age'].min()
        col2.metric('Youngest:', oldest)
    with col3:
        best_vehicle = df1.loc[:, 'Vehicle_condition'].max()
        col3.metric('Best Vehicle:', best_vehicle)
    with col4:
        worst_vehicle = df1.loc[:, 'Vehicle_condition'].min()
        col4.metric('Worst vehicle:', worst_vehicle)

with st.container():
    st.markdown("""___""")
    st.title("Ratings")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### Average Delivery Drivers Rating')
        personnel_ratings = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                             .groupby('Delivery_person_ID')
                             .mean()
                             .reset_index()
                             .round(2))
        personnel_ratings.columns = ['Delivery Person ID', 'Average Rating']

        st.dataframe(personnel_ratings, hide_index=True, height=500)
    with col2:
        st.markdown('##### Average & Standard Deviation Ratings by Traffic Type')
        avg_std = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                   .rename(columns={'Road_traffic_density': 'Road Traffic Density'})
                   .groupby('Road Traffic Density')
                   .agg({'Delivery_person_Ratings': ['mean', 'std']})
                   .round(2))
        avg_std.columns = ['Average', 'Standard Deviation']
        avg_std = avg_std.reset_index()
        avg_std_styled = avg_std.style.background_gradient(cmap='Blues').format(
            {'Average': '{:.2f}', 'Standard Deviation': '{:.2f}'})
        st.dataframe(avg_std_styled, hide_index=True)

        st.markdown('##### Average & Standard Deviation Ratings by Weather Conditions')
        avg_std = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                   .rename(columns={'Weatherconditions': 'Weather Condition'})
                   .groupby('Weather Condition')
                   .agg({'Delivery_person_Ratings': ['mean', 'std']})
                   .round(2))
        avg_std.columns = ['Average', 'Standard Deviation']
        avg_std.reset_index()
        avg_std_styled = avg_std.style.background_gradient(cmap='Blues').format(
            {'Average': '{:.2f}', 'Standard Deviation': '{:.2f}'})
        st.dataframe(avg_std_styled)


with st.container():
    st.markdown("""___""")
    st.title("Delivery Speed Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### Top 10 Fastest Delivery Drivers by City')
        df3 = top_delivers(df1, top_asc=True)
        st.dataframe(df3, hide_index=True)
    with col2:
        st.markdown('##### Top 10 Slowest Delivery Drivers by City')
        df3 = top_delivers(df1, top_asc=False)
        st.dataframe(df3, hide_index=True)


