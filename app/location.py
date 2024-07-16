"""
Reports by Location page for 'I Love My Neighbourhood' App.

Functions:
- Load and display residents' reports from a tracker file.
- Display the reports on a map.
- Display the tracker DataFrame.

Data is stored locally for local deployment and on AWS S3 for 
Streamlit Cloud deployment.
"""

import os

import pandas as pd
import pydeck as pdk
import streamlit as st

from utils import load_tracker_data, get_base64

images_dir = 'images'

# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
cloud = st.session_state.cloud

if cloud:
    s3_bucket = st.session_state.s3_bucket
    s3_client = st.session_state.s3_client
else:
    s3_bucket = None
    s3_client = None


# Load the tracker into a DataFrame
df = load_tracker_data(tracker_file, cloud, s3_client, s3_bucket)  
df.set_index('timestamp', inplace=True) 


st.markdown(
    """
    <div style='text-align: center;'>
        <h1>Reports by Location</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# Get the user's location (fixed for demo purposes)
#current_latitude, current_longitude = get_location()
current_latitude, current_longitude = 51.472, -0.0681

# Create a new DataFrame for the map
map_df = df[
    ['image_path', 'classification', 'latitude', 'longitude', 'comment']
].copy()
map_df['image_path'] = map_df['image_path'].apply(
    lambda x: os.path.join(uploads_dir, x)
)
map_df['image_path'] = map_df['image_path'].apply(
    lambda x: get_base64(x, cloud, s3_client, s3_bucket)
)
map_df['classification'] = map_df['classification'].apply(
    lambda x: f"(classification: {x})"
)

# Add the user's location to the map data
user_icon_path = os.path.join(images_dir, 'user_icon.png')
user_icon_base64 = get_base64(user_icon_path, cloud, s3_client, s3_bucket)
user_location = pd.DataFrame({
    'image_path': [user_icon_base64],
    'classification': ["😀 😀 😀"], 
    'latitude': [current_latitude], 
    'longitude': [current_longitude],
    'comment': ['This is your current location']
})

# Display the map using pydeck
tooltip_html = '''
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_path}" style="max-width: 100px; 
        max-height: 100px;"><br><b>{comment}</b><br>{classification}
    </div>
'''
tooltip = {
    'html': tooltip_html,
    'style': {
        'backgroundColor': 'steelblue',
        'color': 'white',
        'maxWidth': '300px',
        'textAlign': 'center',
        'fontSize': '14px',
    }
}

map_layer = pdk.Layer(
    'ScatterplotLayer',
    data=map_df,
    get_position='[longitude, latitude]',
    get_fill_color='[200, 30, 0, 160]',  # Red for user reports
    get_radius=20,
    pickable=True,
    auto_highlight=True
)

user_layer = pdk.Layer(
    'ScatterplotLayer',
    data=user_location,
    get_position='[longitude, latitude]',
    get_fill_color='[0, 0, 255, 160]',  # Blue for user location
    get_radius=30,  # Larger radius for user location marker
    pickable=True,
    auto_highlight=True
)

view_state = pdk.ViewState(
    latitude=current_latitude, 
    longitude=current_longitude, 
    zoom=14
)

deck = pdk.Deck(
    layers=[map_layer, user_layer], 
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style='mapbox://styles/mapbox/light-v10'
)

st.pydeck_chart(deck)
st.divider()

# Display the tracker DataFrame
st.markdown(
    """
    <div style='text-align: center;'>
    <h3> Residents' Reports </h3>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write(df)
