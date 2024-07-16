""" 
'I Love My Neighbourhood' App. 

This is a simple app designed to engage community members, public 
services, and policymakers in addressing key urban challenges:

- Enhancing urban aesthetics
- Improving community health and well-being
- Promoting sustainability in urban environments
- Ensuring safety in public spaces
- Reducing crime and anti-social behaviour
"""

import os

import boto3
import streamlit as st
from dotenv import load_dotenv
from utils import check_file_exists_on_s3

load_dotenv()
st.session_state.cloud = os.getenv('STREAMLIT_ENV') == 'streamlit-cloud'


def streamlit_deployment():
    """Set up configuration for Streamlit cloud deployment."""
    st.session_state.hf_api_token = st.secrets['HUGGING_FACE_API_TOKEN']
    st.session_state.openai_api_token = st.secrets['OPENAI_API_KEY']
    st.session_state.uploads_dir = "uploads"
    st.session_state.tracker_file = "uploads/tracker.csv"
    st.session_state.s3_bucket = st.secrets['AWS_S3_BUCKET']
    st.session_state.s3_client = boto3.client(
        's3',
        aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'],
        region_name=st.secrets['AWS_REGION']
    )
    
    if not check_file_exists_on_s3(
            st.session_state.s3_client, 
            st.session_state.s3_bucket, 
            st.session_state.tracker_file):
        st.session_state.s3_client.put_object(
            Bucket=st.session_state.s3_bucket, 
            Key=st.session_state.tracker_file, 
            Body=(
                "image_path,classification,timestamp,"
                "latitude,longitude,comment\n"
            )
        )


def local_deployment():
    """Set up configuration for local deployment."""
    st.session_state.hf_api_token = os.getenv('HUGGING_FACE_API_TOKEN')
    st.session_state.openai_api_token = os.getenv('OPENAI_API_KEY')
    st.session_state.uploads_dir = "uploads"
    st.session_state.tracker_file = "uploads/tracker.csv"
    
    if not os.path.exists(st.session_state.uploads_dir):
        os.makedirs(st.session_state.uploads_dir)
        
    if not os.path.exists(st.session_state.tracker_file):
        with open(st.session_state.tracker_file, 'w') as f:
            f.write(
                "image_path,classification,timestamp,"
                "latitude,longitude,comment\n"
            )


if st.session_state.cloud:
    streamlit_deployment()
else:
    local_deployment()
    
# Create pages
upload_photo = st.Page("upload.py", title="Upload Photo", icon="📸")
reports_loc = st.Page("location.py", title="Reports by Location", icon="📍")
trend_analysis = st.Page("trends.py", title="Trend Analysis", icon="📈")
summary_reports = st.Page("summary.py", title="Summary Reports", icon="📝")
admin_panel = st.Page("admin.py", title="Admin Panel", icon="🔧")

# Create navigation menu on sidebar
menu = st.navigation(
    [upload_photo, reports_loc, trend_analysis, summary_reports, admin_panel], 
    position="sidebar"
)

menu.run()
