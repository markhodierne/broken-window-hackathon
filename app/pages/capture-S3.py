import streamlit as st
import uuid
import json
from PIL import Image
from datetime import datetime
import boto3


# Configure AWS S3
s3 = boto3.client('s3')
bucket_name = 'broken-windows'  # Replace with your S3 bucket name

# JSON file to store all metadata
JSON_FILE = 'metadata.json'


def initialize_json_file():
    try:
        s3.get_object(Bucket=bucket_name, Key=JSON_FILE)
    except:
        if e.response['Error']['Code'] == 'NoSuchKey':
            # Object does not exist, create it
            try:
                s3.put_object(Bucket=bucket_name, Key=JSON_FILE, Body=json.dumps([]))
            except:
                print(f"Failed to create {JSON_FILE} in {bucket_name}")
            print(f"Failed to access {JSON_FILE} in {bucket_name}")
            
initialize_json_file()


# Function to save uploaded file and return the file path
def save_uploaded_file(uploaded_file):
    file_id = str(uuid.uuid4())
    file_extension = uploaded_file.name.split(".")[-1]
    file_key = f"{file_id}.{file_extension}"
    try:
        s3.upload_fileobj(uploaded_file, bucket_name, file_key, ExtraArgs={'ACL': 'public-read'})
        file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
        return file_url
    except:
        return None
    
# Streamlit app
st.set_page_config(
        page_title="Neighbourhood Report",
        page_icon="👋",
)

# Initialize session state for metadata
if "metadata" not in st.session_state:
    st.session_state.metadata = []
    

def load_metadata():
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=JSON_FILE)
        metadata = json.loads(obj['Body'].read().decode('utf-8'))
        return metadata
    except:
        print(f"Failed to load metadata from {JSON_FILE} in {bucket_name}")
        return []


if not st.session_state.metadata:
    st.session_state.metadata = load_metadata()


st.title("Neighbourhood Report 👋")
st.sidebar.page_link("pages/weekly_report.py", label="Weekly Report", icon="👋")


# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
comment = st.text_area("Comment here...")
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
location = "long:000 lat:000"
classification = "windows"

if st.button('Submit Comment'):
    if uploaded_file is not None and comment:
        # Save the uploaded file
        image_path = save_uploaded_file(uploaded_file)

        # Append the new metadata to session state
        st.session_state.metadata.append({
            "image_path": image_path,
            "timestamp": timestamp,
            "comment": comment,
            "location": location,
            "classification": classification    
        })

    # Save the updated metadata to the JSON file in S3
    try:
        s3.put_object(Bucket=bucket_name, Key=JSON_FILE, Body=json.dumps(st.session_state.metadata, indent=4))
        st.image(image_url, caption="Uploaded Image", use_column_width=True)
        st.write("Comment:", comment)
        st.success("Thanks for caring about your neighbourhood. Your photo and comment have been saved.")
    except:
        st.error("Failed to save your comment. Please try again later.")
else:
    st.error("Failed to upload the image. Please try again later.")

# Run Streamlit app using 'streamlit run app.py' command
