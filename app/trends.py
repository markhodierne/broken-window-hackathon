"""
Trend Analysis page for 'I Love My Neighbourhood' App.

Functions:
- Load and display residents' reports from a tracker file.
- Filter reports by category and visualize them over time.
- Display filtered reports in a tabular format.

Data is stored locally for local deployment and on AWS S3 for 
Streamlit Cloud deployment.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils import load_tracker_data


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


# Display the page title       
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>Reports Over Time by Category</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# Load the tracker into a DataFrame
df = load_tracker_data(tracker_file, cloud, s3_client, s3_bucket)  
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])
df.set_index('timestamp', inplace=True)

# Select category
categories = sorted(df['classification'].unique())
selected_category = st.selectbox('Select Category', categories)
st.write("")

# Filter data by selected category
df_filtered = df[df['classification'] == selected_category]

# Resample by week to count reports
reports_per_week = df_filtered['comment'].resample('W').count()

# Resample by month to count comments
reports_per_month = df_filtered['comment'].resample('ME').count()

# Create two columns for side-by-side plots
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <h3 style="text-align: center;">Reports per Week<br>
        ({selected_category})</h3>
        """,
        unsafe_allow_html=True
    )
    fig_week, ax_week = plt.subplots(figsize=(5, 3))
    ax_week.plot(
        reports_per_week.index, reports_per_week, 
        marker='o', color='teal', label='Reports per Week'
    )
    ax_week.set_ylabel('Number of Reports')
    ax_week.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_week)

with col2:
    st.markdown(
        f"""
        <h3 style="text-align: center;">
            Reports per Month<br>({selected_category})
        </h3>
        """,
        unsafe_allow_html=True
    )
    fig_month, ax_month = plt.subplots(figsize=(5, 3))
    ax_month.plot(
        reports_per_month.index, reports_per_month, 
        marker='o', color='darkred', label='Reports per Month'
    )
    ax_month.set_ylabel('Number of Reports')
    ax_month.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig_month)

# Display the tracker DataFrame filtered by selected category
st.write("")
st.markdown(
    """
    <div style='text-align: center;'>
        <h3> Residents' Reports </h3>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write(df_filtered)
