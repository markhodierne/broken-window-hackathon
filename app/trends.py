# Import the required libraries and modules
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
cloud = st.session_state.cloud
if cloud:
    s3_bucket = st.session_state.s3_bucket
    s3_client = st.session_state.s3_client

    # Function to read CSV tracker file from S3
    def read_csv_from_s3(bucket_name, object_key):
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            csv_content = response['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            return df
        except Exception as e:
            st.write(f"Failed to read CSV from S3. Reason: {e}")
            return None
        
        
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
if cloud:
    df = read_csv_from_s3(s3_bucket, tracker_file)  
else:
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
    st.markdown(
        f"""
        <h3 style="text-align: center;">Reports per Week<br>({selected_category})</h3>
        """,
        unsafe_allow_html=True
    )
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
    st.markdown(
        f"""
        <h3 style="text-align: center;">Reports per Month<br>({selected_category})</h3>
        """,
        unsafe_allow_html=True
    )
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

# Display the tracker DataFrame filtered by selected category
st.write("")
st.markdown("""
<div style='text-align: center;'>
    <h3> Residents' Reports </h3>
</div>
""", unsafe_allow_html=True)
st.write(df_filtered)