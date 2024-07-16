"""
Admin Panel page for 'I Love My Neighbourhood' App.

Functions:
- Backup all residents' reports.
- Download a backup of residents' reports.
- Delete all existing residents' reports.
- Delete all existing residents' reports and load sample reports.

Data is stored locally for local deployment and on AWS S3 for 
Streamlit Cloud deployment.
"""

import streamlit as st

from utils import delete_dir, add_sample_data


sample_data_dir = "sample_data"

# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
cloud = st.session_state.cloud

if cloud:
    s3_bucket = st.session_state.s3_bucket
    s3_client = st.session_state.s3_client


# Display the admin panel title
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>Admin Panel</h1>
    </div>
    """, 
    unsafe_allow_html=True
)
st.divider()
st.markdown(
    """
    ##### Admin actions:
    - Backup all residents' reports.
    - Download a backup of residents' reports.
    """, 
    unsafe_allow_html=True
)
st.write("")
st.markdown(
    """
    ##### WARNING: The following actions will delete ALL existing data:
    - Delete all existing residents' reports.
    - Delete all existing residents' reports and load sample reports.
    """, 
    unsafe_allow_html=True
)
st.write("")

# Define the options
option1 = "Backup all residents' reports (unavailable)"
option2 = "Download a backup of residents' reports (unavailable)"
option3 = "Delete all existing residents' reports"
option4 = "Delete all existing residents' reports and load sample reports"

# Define available and unavailable options
all_options = [option1, option2, option3, option4]
available_options = [option3, option4]
disabled_options = [option1, option2]

with st.form(key='admin_action'):
    option = st.selectbox('Select an option:',(all_options))
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if option == option3 or option == option4:
        delete_dir(uploads_dir, cloud, s3_client, s3_bucket)
        if option == option4:
            add_sample_data(
                sample_data_dir, uploads_dir, cloud, s3_client, s3_bucket
            )
    elif option in disabled_options:
        st.write("This action is not yet available.")
            