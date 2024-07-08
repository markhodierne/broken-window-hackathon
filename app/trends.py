# Import the required libraries and modules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file


st.markdown(
    """
    <div style='text-align: center;'>
    <h1>Reports Over Time by Category</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# Load the tracker
df = pd.read_csv(tracker_file)

# Convert timestamp to datetime without specifying a format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop any rows with NaT values
df = df.dropna(subset=['timestamp'])

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Select category
categories = sorted(df['classification'].unique())
selected_category = st.selectbox('Select Category', categories)
st.write("")

# Filter data by selected category
df_filtered = df[df['classification'] == selected_category]

# Resample by week to count reports
comments_per_week = df_filtered['comment'].resample('W').count()

# Resample by month to count comments
comments_per_month = df_filtered['comment'].resample('ME').count()

# Create two columns for side-by-side plots
col1, col2 = st.columns(2)

with col1:
    st.subheader(f'Reports per Week ({selected_category})')
    fig_week, ax_week = plt.subplots(figsize=(5, 3))
    ax_week.plot(
        comments_per_week.index, comments_per_week, 
        marker='o', color='teal', label='Reports per Week'
    )
    ax_week.set_ylabel('Number of Reports')
    ax_week.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_week)

with col2:
    st.subheader(f'Reports per Month ({selected_category})')
    fig_month, ax_month = plt.subplots(figsize=(5, 3))
    ax_month.plot(
        comments_per_month.index, comments_per_month, 
        marker='o', color='darkred', label='Reports per Month'
    )
    ax_month.set_ylabel('Number of Reports')
    ax_month.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_month)

# Display the DataFrame
st.write("")
st.markdown("""
<div style='text-align: center;'>
    <h3> Residents' Reports </h3>
</div>
""", unsafe_allow_html=True)
st.write(df_filtered)