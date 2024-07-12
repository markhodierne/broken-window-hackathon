import os
import shutil

import streamlit as st


sample_data_dir = "sample_data"

# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
s3_bucket = st.session_state.s3_bucket
s3_client = st.session_state.s3_client
cloud = st.session_state.cloud


def delete_dir_local(uploads_dir):
    try:
        if os.path.exists(uploads_dir):
            shutil.rmtree(uploads_dir)
            st.write('All reports have been deleted successfully.')
    except Exception as e:
        st.write(f"Failed to delete all reports. Reason: {e}")


def delete_dir_s3(bucket_name):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for item in response['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=item['Key'])
            st.write('All reports have been deleted successfully.')
    except Exception as e:
        st.write(f"Failed to delete all reports. Reason: {e}")


def add_sample_data_local(sample_data_dir):
    try:
        if os.path.exists(sample_data_dir) and os.path.isdir(sample_data_dir):
            shutil.copytree(sample_data_dir, uploads_dir)
            st.write('Sample reports have been loaded successfully.')
    except Exception as e:
        st.write(f"Failed to create sample reports. Reason: {e}")


def add_sample_data_s3(bucket_name, sample_data_prefix, uploads_prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=sample_data_prefix)
        if 'Contents' not in response:
            st.write(f"No sample data found at {sample_data_prefix}.")
            return

        for obj in response['Contents']:
            source_key = obj['Key']
            new_key = uploads_prefix + source_key[len(sample_data_prefix):]
            copy_source = {'Bucket': bucket_name, 'Key': source_key}
            s3_client.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=new_key)
        st.write('Sample reports have been loaded successfully.')
    except Exception as e:
        st.write(f"Failed to create sample reports. Reason: {e}")



st.markdown("""
<div style='text-align: center;'>
    <h1>Admin Panel</h1>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown(
    """
    ##### Admin actions:
    - Backup residents' reports.
    - Download a backup of residents' reports.
    """, 
    unsafe_allow_html=True
)
st.write("")
st.markdown(
    """
    ##### WARNING: The following actions will delete ALL existing data:
    - Reset the app with no resident's reports.
    - Reset the app and then load with sample residents' reports.
    """, 
    unsafe_allow_html=True
)
st.write("")

# Define the options
option1 = "Backup residents' reports (unavailable)"
option2 = "Download backup (unavailable)"
option3 = "Delete all existing residents' reports"
option4 = "Delete existing and re-load sample reports"

# Define available and unavailable options
all_options = [option1, option2, option3, option4]
available_options = [option3, option4]
disabled_options = [option1, option2]

with st.form(key='admin_action'):
    option = st.selectbox('Select an option:',(all_options))
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if option == option3 or option == option4:
        if cloud:
            delete_dir_s3(s3_bucket)
        else:
            delete_dir_local(uploads_dir)
        
        if option == option4:
            if cloud:
                add_sample_data_s3(s3_bucket, sample_data_dir, uploads_dir)
            else:
                add_sample_data_local(sample_data_dir, uploads_dir)
    elif option in disabled_options:
        st.write("This action is not yet available.")
