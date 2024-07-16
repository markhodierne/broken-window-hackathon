"""
Upload Photo page for 'I Love My Neighbourhood' App.

Functions:
- Upload a photo and add a comment.
- Classify the photo using OpenAI's CLIP model.
- Save the photo and photo metadata.
- Display the photo and metadata.
- Display information about the project.

Data is stored locally for local deployment and on AWS S3 for 
Streamlit Cloud deployment.
"""

import base64
from datetime import datetime
from io import BytesIO

import streamlit as st

from utils import query, get_location, save_image_data, save_uploaded_file


# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
api_token = st.session_state.hf_api_token
cloud = st.session_state.cloud
if cloud:
    s3_bucket = st.session_state.s3_bucket
    s3_client = st.session_state.s3_client

# Hugging Face Inference API URL for clip-vit-base-patch32
API_URL = (
    "https://api-inference.huggingface.co/"
    "models/openai/clip-vit-base-patch32"
)
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

def classify_image(image, categories, threshold=0.5):
    """
    Classify the image using OpenAI's CLIP model.

    Args:
        image (PIL.Image.Image): The image to classify.
        categories (list): List of categories for classification.
        threshold (float): The score threshold to determine the 
            classification.

    Returns:
        str: The predicted category.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    payload = {
        "inputs": {"image": img_str},
        "parameters": {"candidate_labels": categories}
    }

    data = query(payload, API_URL, headers)
    
    predicted_category = "other"
    
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        scores = [item['score'] for item in data]
        labels = [item['label'] for item in data]
        max_score = max(scores)
        if max_score >= threshold:
            predicted_category = labels[scores.index(max_score)]
    else:
        st.write("Failed to classify image or no valid response from API.")
    return predicted_category
        

# Display the app title
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>I ❤️ My Neighbourhood</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()
st.write(
    """
    Report any issues in our neighbourhood by uploading a photo...
    """, 
    unsafe_allow_html=True
)

# Create a form for image and comment and submission
with st.form(key='image_comment_form'):
    uploaded_image = st.file_uploader(
        "Upload file", 
        type=['png', 'jpg', 'jpeg', 'webp', 'heic']
    )
    comment = st.text_input("Add a comment about the image:")
    submit_button = st.form_submit_button(label="Submit photo and comment")

# Check if the form was submitted
if submit_button:    
    if uploaded_image is not None and comment:
        st.write('Submitting your report...')
        
        # Save the image
        image_path, resized_image = save_uploaded_file(
            uploaded_image, uploads_dir, cloud, s3_client, s3_bucket
        )
        # Get classification, timestamp and location
        classification = classify_image(resized_image, categories, threshold=0.5)
        timestamp_raw = datetime.now()
        timestamp = timestamp_raw.strftime("%Y-%m-%d %H:%M:%S")
        latitude, longitude = get_location()
        
        # Save the image metadata
        cleaned_comment = comment.replace(',', '') # Remove commas
        save_image_data(
            image_path, classification, timestamp, latitude, longitude, 
            cleaned_comment, tracker_file, cloud, s3_client, s3_bucket 
        )
        st.write(f'Successful submission. Thank you for your report!')

        # Display the resized image
        st.image(resized_image, caption='', use_column_width=False)
        
        st.write(
            f"""
            <div style="background-color:#b1d4f0;
            padding:10px;border-radius:5px">
            Photo Category:  {classification}<br>
            Comment:  {comment}<br>
            Time: {timestamp} Location: {latitude}, {longitude}
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.write("Please upload an image and add a comment before submitting.")

st.write("")

# Create an expander for project information
with st.expander("About the Project"):
    st.markdown(
        """
                
        **"I Love My Neighbourhood"** is a simple app designed to engage 
        community members, public services and policymakers in 
        addressing key urban challenges:

        - Enhancing urban aesthetics
        - Improving community health and well-being
        - Promoting sustainability in urban environments
        - Ensuring safety in public spaces
        - Reducing crime and anti-social behaviour

        This 'proof of concept' app was developed during a hackathon 
        organized by Future London with contributions from policymakers 
        and tech enthusiasts. Ultimately, the app would be deployed on 
        mobile devices, either as a stand-alone app or as an AI bot for 
        existing WhatsApp community groups.

        Users are able to submit photos and/or comments about their 
        local neighbourhood - things they love, like green spaces, 
        public buildings, and community activities - and things they 
        don't love, like graffiti, fly tipping, and broken windows. AI 
        is leveraged to classify and analyze these reports - and track 
        how things are changing over time.

        Such data provides insights about local urban issues, and 
        empowers residents to work effectively with public services and 
        voluntary bodies to make improvements. The data also helps 
        policymakers to see the bigger picture, helping them decide 
        which problems are critical, and allocate resources accordingly.
        This is Broken Window Theory in action ... grass roots fashion.
        
        The app is only designed to recognize photos in 6 different 
        categories:

        - **Graffiti**: Art or vandalism?
        - **Garbage**: Addressing waste management and cleanliness in 
        urban areas.
        - **Broken Windows**: Studying the effects of urban decay and 
        vandalism.
        - **Green Spaces**: Promoting parks and natural areas for 
        community well-being.
        - **Public Buildings**: Evaluating the use and maintenance of 
        public infrastructure.
        - **Sports and Social Events**: Encouraging physical activities, 
        social gatherings and events in neighborhoods.
        """
    )
