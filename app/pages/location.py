# Import the required libraries and modules
import os
import base64
import pandas as pd
import pydeck as pdk
import streamlit as st
from PIL import Image


# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
images_dir = 'images'

# Load the tracker
df = pd.read_csv(tracker_file)
df.set_index('timestamp', inplace=True)


# Function to format the thumbnail path
def get_thumb_path(filename, dir):
    base_filename = os.path.basename(filename)
    name, ext = base_filename.rsplit('.', 1)
    thumb_filename = f"{name}_thumb.{ext}"
    return os.path.join(dir, thumb_filename)
    
# Function to format image as base64
def get_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
    

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
map_df = df[['image_path', 'classification', 'latitude', 'longitude', 'comment']].copy()
map_df.columns = ['thumbnail', 'category', 'lat', 'lon', 'comment']
map_df['thumbnail'] = map_df['thumbnail'].apply(lambda x: get_thumb_path(x, uploads_dir))
map_df['thumbnail'] = map_df['thumbnail'].apply(get_base64)

# Apply formatting to 'category' and 'comment' columns
map_df['category'] = map_df['category'].apply(lambda x: f"(Category: {x})")

# Add the user's location to the map data
user_icon_path = os.path.join(images_dir, 'user_icon.png')
user_icon_base64 = get_base64(user_icon_path)

user_location = pd.DataFrame(
    {'thumbnail': [user_icon_base64],
    'category': ["😀 😀 😀"], 
    'lat': [current_latitude], 
    'lon': [current_longitude],
    'comment': ['This is your current location']
    }
)

# Display the map using pydeck
tooltip_html = '''
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{thumbnail}" style="max-width: 100px; 
        max-height: 100px;"><br><b>{comment}</b><br>{category}
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
    get_position='[lon, lat]',
    get_fill_color='[200, 30, 0, 160]',  # Red for user reports
    get_radius=20,
    pickable=True,
    auto_highlight=True
)

user_layer = pdk.Layer(
    'ScatterplotLayer',
    data=user_location,
    get_position='[lon, lat]',
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