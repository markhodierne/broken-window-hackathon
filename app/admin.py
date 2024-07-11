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
        if os.path.exists(uploads_dir):
            try:
                shutil.rmtree(uploads_dir)
                st.write('All reports have been deleted successfully.')
            except Exception as e:
                    print(f"Failed to delete all reports. Reason: {e}")
        if option == option4:
            if os.path.exists(sample_data_dir) and os.path.isdir(sample_data_dir):
                try:
                    shutil.copytree(sample_data_dir, uploads_dir)
                    st.write('Sample reports have been loaded successfully.')
                except Exception as e:
                    print(f"Failed to load sample reports. Reason: {e}")
    elif option in disabled_options:
        st.write("This action is not yet available.")
