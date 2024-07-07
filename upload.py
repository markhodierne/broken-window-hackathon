# Import the required libraries and modules
import os
import uuid
import base64
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval

# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
api_token = st.session_state.api_token

# Hugging Face Inference API URL for CLIP
API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
headers = {"Authorization": f"Bearer {api_token}"}

# Define categories
categories = [
    "graffiti",
    "garbage",
    "broken_window",
    "green_spaces",
    "public_buildings",
    "sports_and_social_events"
]

threshold = 0.5  # Set a threshold for classifying as "Other"


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Function to get user's location based on IP address
def XXXget_user_location():
    response = requests.get("https://ipinfo.io")
    data = response.json()
    location = data['loc'].split(',')
    latitude = float(location[0])
    longitude = float(location[1])
    return latitude, longitude


# Function to get user's location
def get_user_location():
    loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(function(position) { return [position.coords.latitude, position.coords.longitude]; })', key='geolocation')
    
    if loc:
        latitude, longitude = loc
        st.write(f"Latitude: {latitude}, Longitude: {longitude}")
        return latitude, longitude
    else:
        return None, None


# Function to save uploaded file and return the file path
def save_uploaded_file(uploaded_file):
    file_id = str(uuid.uuid4())
    file_extension = uploaded_file.name.split(".")[-1]
    file_name = f"{file_id}.{file_extension}"
    file_path = os.path.join(uploads_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_name


# Function to save image data to tracker
def save_image_data(image_path, classification, timestamp, latitude, longitude, comment):
    with open(tracker_file, 'a') as f:
        f.write(f"{image_path},{classification},{timestamp},{latitude},{longitude},{comment}\n")
    return


def classify_image(image, categories, threshold=0.2):
    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Query the API with category labels
    payload = {
        "inputs": {"image": img_str},
        "parameters": {"candidate_labels": categories}
    }
    data = query(payload)
    
    # Default value for predicted category
    predicted_category = "other"
    
    # Process the response
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        scores = [item['score'] for item in data]
        labels = [item['label'] for item in data]
        max_score = max(scores)
        if max_score >= threshold:
            predicted_category = labels[scores.index(max_score)]

    return predicted_category
        

# Display the app title
st.title("I ❤️ My Neighbourhood")
st.write("")
st.write(f'''
            <div>
                NOTE : This 'proof of concept' app is designed to recognize only these 6 categories of photo:<br>
                Green Spaces, Public Buildings, Sports and Social Events, Graffiti, Garbage, and Broken Windows<br>
                (3 things the community loves; 3 things that need fixing)
            </div>
            ''', unsafe_allow_html=True)
st.write("")
st.write("<strong>Report any issues in our neighbourhood by uploading a photo...</strong>", unsafe_allow_html=True)

# Create a form for the comment and submission
with st.form(key='image_comment_form'):
    # Upload image
    uploaded_image = st.file_uploader("Upload file", type=['png', 'jpg', 'jpeg', 'webp', 'heic'])

    # Create a comment input box inside the form
    comment = st.text_input("Add a comment about the image:")
    
    # Create Submit button inside the form
    submit_button = st.form_submit_button(label="Submit photo and comment")

# Check if the form was submitted
if submit_button:    
    # Process the uploaded image and comment
    if uploaded_image is not None and comment:
        # Display the comment and the image
        st.write(f'Thank you for your report!')
        
        # Open the uploaded image
        image = Image.open(uploaded_image)
        
        # Save the image
        image_path = save_uploaded_file(uploaded_image)
        
        # Get classification, timestamp and location
        classification = classify_image(image, categories, threshold=threshold)
        #timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        #formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.now()
        latitude, longitude = get_user_location()
        
        # Save the image metadata
        cleaned_comment = comment.replace(',', '') # Remove commas from the comment
        save_image_data(image_path, classification, timestamp, latitude, longitude, cleaned_comment)

        # Calculate the new size while maintaining the aspect ratio
        smallest_dimension = 300
        original_width, original_height = image.size
        if original_width < original_height:
            new_width = smallest_dimension
            new_height = int((smallest_dimension / original_width) * original_height)
        else:
            new_height = smallest_dimension
            new_width = int((smallest_dimension / original_height) * original_width)
            
        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)

        # Display the resized image
        st.image(resized_image, caption='', use_column_width=False)
        
        # Use st.write with HTML for multi-line success message
        st.write(f'''
            <div style="background-color:#E6FAE4;padding:10px;border-radius:5px">
                Photo Category:  {classification}<br>
                Comment:  {comment}<br>
                Time:  {timestamp}   Location:  {latitude}, {longitude}
            </div>
            ''', unsafe_allow_html=True)
        
    else:
        st.write("Please upload an image and add a comment before submitting.")
