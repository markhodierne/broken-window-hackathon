import streamlit as st
import pandas as pd
import pydeck as pdk


# Load the session state variables
tracker_file = st.session_state.tracker_file

# Load the tracker
df = pd.read_csv(tracker_file)
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
map_df = df[['latitude', 'longitude', 'classification', 'comment']].copy()
map_df.columns = ['lat', 'lon', 'category', 'comment']

# Apply formatting to 'category' and 'comment' columns
map_df['category'] = map_df['category'].apply(lambda x: f"(Category: {x})")

# Add the user's location to the map data
user_location = pd.DataFrame(
    {'lat': [current_latitude], 
    'lon': [current_longitude], 
    'category': ["😀 😀 😀"], 
    'comment': ['This is your current location']
    }
)

# Display the map using pydeck
tooltip = {
    'html': '<b>{comment}</b><br>{category}',
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
