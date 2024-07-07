# Import the required libraries and modules
import os
import uuid
import base64
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from datetime import datetime
import streamlit.components.v1 as components


# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
api_token = st.session_state.hf_api_token

# Hugging Face Inference API URL for clip-vit-base-patch32
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

# Global variables
latitude = None
longitude = None
threshold = 0.5  # Set a threshold for classifying as "Other"


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# Function to get user's location based on IP address
def get_location():
    response = requests.get("https://ipinfo.io")
    data = response.json()
    location = data['loc'].split(',')
    latitude = float(location[0])
    longitude = float(location[1])
    return latitude, longitude


def XXXget_location():
    loc = components.html(
        """
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            } else {
                document.getElementById('location').innerHTML = "Geolocation is not supported by this browser.";
            }
        }

        function showPosition(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            document.getElementById('location').innerHTML = lat + "," + lon;
            const streamlitMessage = new CustomEvent("streamlit:location", {
                detail: {latitude: lat, longitude: lon},
            });
            window.dispatchEvent(streamlitMessage);
        }
        getLocation();
        
        window.addEventListener("streamlit:location", (event) => {
            const latitude = event.detail.latitude;
            const longitude = event.detail.longitude;
            Streamlit.setComponentValue({latitude: latitude, longitude: longitude});
        });
        </script>
        <p id="location"></p>
        """,
        height=200,
    )
    return loc


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
        

'''
st.title('Location App')

# Capture location data
location_data = get_location()

# Initialize session state for latitude and longitude if not already set
if 'latitude' not in st.session_state:
    st.session_state.latitude = None
if 'longitude' not in st.session_state:
    st.session_state.longitude = None

# Update session state with the location data if available
if location_data and 'latitude' in location_data and 'longitude' in location_data:
    st.session_state.latitude = location_data['latitude']
    st.session_state.longitude = location_data['longitude']

# Display the location data if available
if st.session_state.latitude and st.session_state.longitude:
    st.write(f"Latitude: {st.session_state.latitude}")
    st.write(f"Longitude: {st.session_state.longitude}")
else:
    st.write("Fetching location...")

# Debug: Display the entire session state (optional)
st.write(st.session_state)
'''
        

# Display the app title
st.markdown("""
<div style='text-align: center;'>
    <h1>I ❤️ My Neighbourhood</h1>
</div>
""", unsafe_allow_html=True)

st.divider()

st.write("")
st.write("Report any issues in our neighbourhood by uploading a photo...", unsafe_allow_html=True)

# Create a form for image and comment and submission
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
        latitude, longitude = get_location()
        
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

st.write("")

# Create an expander for project information
with st.expander("About the Project"):
    st.markdown("""
                
    **"I Love My Neighbourhood"** is a simple app designed to engage community members, 
    public services and policymakers in addressing key urban challenges:

    - Enhancing urban aesthetics
    - Improving community health and well-being
    - Promoting sustainability in urban environments
    - Ensuring safety in public spaces
    - Reducing crime and anti-social behaviour

    This 'proof of concept' app was developed during a hackathon organized by Future London 
    with contributions from policymakers and tech enthusiasts. Ultimately, the app would 
    be deployed on mobile devices, either as a stand-alone app or as an AI bot for existing 
    WhatsApp community groups.

    Users are able to submit photos and/or comments about their local neighbourhood - 
    things they love, like green spaces, public buildings, and community activities - 
    and things they don't love, like graffiti, fly tipping, and broken windows. 
    AI is leveraged to classify and analyze these reports - and track how things are 
    changing over time.

    Such data provides insights about local urban issues, and empowers residents to work 
    effectively with public services and voluntary bodies to make improvements. 
    The data also helps policymakers to see the bigger picture, helping them decide which 
    problems are critical, and allocate resources accordingly.This is Broken Window Theory 
    in action ... grass roots fashion.
    
    The app is only designed to recognize photos in 6 different categories:

    - **Graffiti**: Art or vandalism?
    - **Garbage**: Addressing waste management and cleanliness in urban areas.
    - **Broken Windows**: Studying the effects of urban decay and vandalism.
    - **Green Spaces**: Promoting parks and natural areas for community well-being.
    - **Public Buildings**: Evaluating the use and maintenance of public infrastructure.
    - **Sports and Social Events**: Encouraging physical activities, social gatherings and events in neighborhoods.
    """)
