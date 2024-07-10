# Import the required libraries and modules
import streamlit as st



# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file



st.markdown("""
<div style='text-align: center;'>
    <h1>Admin Panel</h1>
</div>
""", unsafe_allow_html=True)

st.divider()
st.write(
    "The actions on this page are illustrative and are not functional in this " 
    "demo."
)
st.write("")
st.markdown(
    """
    ##### Admin actions:
    1. Backup residents' reports.
    
    2. Download a backup of residents' reports.
    """, 
    unsafe_allow_html=True
)
st.write("")
st.markdown(
    """
    ##### WARNING: The following actions will delete ALL existing data:
    3. Reset the app with no resident's reports.
    
    4. Reset the app and then load with sample residents' reports.
    """, 
    unsafe_allow_html=True
)
