import streamlit as st
from PIL import Image
st.set_page_config(
    page_title='Home',
    page_icon='🥡'
)


#image_path = 'C:/Users/amand/Code/repos/ftc_python/'
image = Image.open('logo.jpg')
st.sidebar.image(image, use_column_width=True)

st.sidebar.markdown("# **:blue[Curry Company]**")
st.sidebar.markdown("## *Fastest Delivery in Town*")
st.sidebar.markdown("""---""")

st.write('# **:blue[Curry Company]** *Metrics Dashboard*')

st.markdown(
    """
    Growth Dashboard Overview
    Purpose: The Growth Dashboard is created to monitor the growth metrics of delivery personnel and restaurants.
    
    --> ***How to Use the Dashboard?*** <--
    
    1. **Company Overview**:
        - Manager View: Provides general __behavioral__ metrics.
        - Strategic View: Displays __weekly__ __growth__ indicators.
        - Geographical View: Offers insights based on __geolocation__.
        
    2. **Delivery Drivers View**:
        Tracks weekly growth indicators specific to delivery drivers.
        
    3. **Restaurant View**:
        Shows weekly growth indicators for restaurants.  
        
         
    ***Assistance:
    For any queries or assistance with the dashboard, you can contact the responsible Data Scientist:
    [Amanda Rodrigues](https://www.amandarc.dev)***
    """)
