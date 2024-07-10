""" I Love My Neighbourhood App. 

This is a simple app designed to engage community members, public 
services and policymakers in addressing key urban challenges:

- Enhancing urban aesthetics
- Improving community health and well-being
- Promoting sustainability in urban environments
- Ensuring safety in public spaces
- Reducing crime and anti-social behaviour
"""

# Import the required libraries and modules
import os
import streamlit as st
import boto3
from dotenv import load_dotenv


# Uncomment when figuring out!!
#s3_client = init_s3_client()
#s3_bucket = st.secrets['AWS_S3_BUCKET']


# Check if a "directory" exists
def check_directory_exists(s3_client, bucket, prefix):
    result = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
    return 'Contents' in result


# Create a "directory" by uploading a zero-byte object
def create_directory(s3_client, bucket, prefix):
    s3_client.put_object(Bucket=bucket, Key=f"{prefix}/")


# Check if a file exists
def check_file_exists(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


# Upload a file to S3
def upload_file(s3_client, bucket, key, file_obj):
    s3_client.upload_fileobj(file_obj, bucket, key)
    
    
def streamlit_deployment():
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
    # Image directory setup
    if not check_directory_exists(
            st.session_state.s3_client, st.session_state.s3_bucket, 
            uploads_dir):
        
        create_directory(
            st.session_state.s3_client, 
            st.session_state.s3_bucket, 
            uploads_dir
        )
    
    # Data tracker setup
    if not check_file_exists(
            st.session_state.s3_client, st.session_state.s3_bucket, 
            tracker_file):
        
        st.session_state.s3_client.put_object(
            Bucket=st.session_state.s3_bucket, 
            Key=tracker_file, 
            Body="""
                image_path,classification,timestamp,latitude,longitude,
                comment\n
            """
        )


def local_deployment():
    load_dotenv()
    st.session_state.hf_api_token = os.getenv('HUGGING_FACE_API_TOKEN')
    st.session_state.openai_api_token = os.getenv('OPENAI_API_KEY')
    st.session_state.uploads_dir = "uploads"
    st.session_state.tracker_file = "uploads/tracker.csv"
    
    # Image directory setup
    if not os.path.exists(st.session_state.uploads_dir):
        os.makedirs(st.session_state.uploads_dir)
        
    # Data tracker setup
    if not os.path.exists(st.session_state.tracker_file):
        with open(st.session_state.tracker_file, 'w') as f:
            f.write(
                "image_path,classification,timestamp,"
                "latitude,longitude,comment\n"
            )





st.session_state.cloud = os.getenv('STREAMLIT_ENV') == 'streamlit'

if st.session_state.cloud:
    streamlit_deployment()
else:
    local_deployment()
    
# Create pages
upload_photo = st.Page(
    "upload.py", 
    title="Upload Photo", 
    icon="📸"
)
reports_location = st.Page(
    "location.py", 
    title="Reports by Location", 
    icon="📍"
)
trend_analysis = st.Page(
    "trends.py", 
    title="Trend Analysis", 
    icon="📈"
)
summary_reports = st.Page(
    "summary.py", 
    title="Summary Reports", 
    icon="📝"
)
admin_panel = st.Page(
    "admin.py", 
    title="Admin Panel", 
    icon="🔧"
)

# Create navigation menu on sidebar
menu = st.navigation(
    [upload_photo, reports_location, 
    trend_analysis, summary_reports, admin_panel], 
    position="sidebar"
)

menu.run()
