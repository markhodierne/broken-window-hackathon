import streamlit as st
import os
import uuid
import json
from PIL import Image
from datetime import datetime

# Directory to save uploaded images
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# JSON file to store all metadata
JSON_FILE = UPLOAD_DIR + "metadata.json"

# Initialize the JSON file if it doesn't exist
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as f:
        json.dump([], f)

# Function to save uploaded file and return the file path
def save_uploaded_file(uploaded_file):
    file_id = str(uuid.uuid4())
    file_extension = uploaded_file.name.split(".")[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{file_extension}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Initialize session state for metadata
if "metadata" not in st.session_state:
    st.session_state.metadata = []

# Load existing metadata from JSON file into session state
if os.path.exists(JSON_FILE) and not st.session_state.metadata:
    with open(JSON_FILE, "r") as f:
        st.session_state.metadata = json.load(f)

# Streamlit app
st.set_page_config(
        page_title="Neighbourhood Report",
        page_icon="👋",
    )

st.title("Neighbourhood Report 👋")
st.sidebar.page_link("pages/weekly_report.py", label="Weekly Report", icon="👋")


# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
comment = st.text_area("Comment here...")
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
location = "long:000 lat:000"

if st.button('Submit Comment'):
    if uploaded_file is not None and comment:
        # Save the uploaded file
        image_path = save_uploaded_file(uploaded_file)

        # Append the new metadata to session state
        st.session_state.metadata.append({
            "image_path": image_path,
            "timestamp": timestamp,
            "comment": comment,
            "location": location
        })

    # Save the updated metadata to the JSON file
    with open(JSON_FILE, "w") as f:
        json.dump(st.session_state.metadata, f, indent=4)

    # Display the uploaded image and comment
    st.image(image_path, caption="Uploaded Image", use_column_width=True)
    st.write("Comment:", comment)
    st.success("Thanks for caring about your neighbourhood. Your photo and comment have been saved.")

# Run Streamlit app using 'streamlit run app.py' command
