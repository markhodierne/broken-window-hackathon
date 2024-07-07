import streamlit as st
import os
import uuid
import csv
from PIL import Image
from datetime import datetime
from transformers import CLIPProcessor, CLIPModel
import pandas as pd

#from openai import OpenAI
#from dotenv import load_dotenv

# Create an instance of the OpenAI class
#load_dotenv()
#client = OpenAI()


# Set OpenAI API key
#api_key = st.secrets["openai"]["api_key"]
#if api_key is None:
#    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
#openai.api_key = api_key

# Define categories
categories = [
    "graffiti",
    "garbage",
    "broken_window",
    "green_spaces",
    "public_buildings",
    "sports_and_social_events"
]

# Directory setup for images
uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# Data tracker setup
tracker_file = "tracker.csv"
tracker_path = os.path.join(uploads_dir, tracker_file)
if not os.path.exists(tracker_path):
    with open(tracker_path, 'w') as f:
        f.write("image_path,classification,timestamp,latitude,longitude,comment\n")
        

# Function to save uploaded file and return the file path
def save_uploaded_file(uploaded_file):
    file_id = str(uuid.uuid4())
    file_extension = uploaded_file.name.split(".")[-1]
    file_path = os.path.join(uploads_dir, f"{file_id}.{file_extension}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

'''
# Function to classify image
def classify_image(image):
    # Convert the image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Classify this image mostly into one of the following categories: graffiti, garbage, broken_window, green_spaces, public_buildings, sports_and_social_events, other. Respond with only the category name."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=10
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        st.error(f"Error classifying image: {str(e)}")
        return None


# MAIN

if uploaded_file is not None:
    if image_name.endswith(('.png', '.jpg', '.jpeg')):  # check for image files
        path = os.path.join(image_dir, image_name)
        image = Image.open(path)
        
        # Need????
        # Resize the image to half its original size
        #original_size = image.size
        #new_size = (int(w_size), int(h_size))
        #resized_image = image.resize(new_size)
        
        # Display the image
        st.image(image, caption='Uploaded Image.', use_column_width=False)

        # Preprocess image and prepare text inputs
        inputs = processor(text=categories, images=image, return_tensors="pt", padding=True)

        # Model prediction
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image  # this is the image -> text similarity score
        probs = logits_per_image.softmax(dim=1)  # we apply softmax to normalize the scores

        # Get the highest probability category
        best_category = categories[probs.argmax().item()]

        # Store result
        results[image_name] = best_category
'''



# Streamlit app
#st.set_page_config(
#        page_title="Neighbourhood Report",
#        page_icon="👋",
#    )

# Initialize session state for metadata
if "tracker" not in st.session_state:
    st.session_state.tracker = []
    
# Load data from tracker file into session state
if os.path.exists(tracker_path) and not st.session_state.tracker:
    with open(tracker_path, "r") as f:
        reader = csv.reader(f)
        st.session_state.tracker = list(reader)

# Display the app title and sidebar
st.title("Neighbourhood Report 👋")
st.sidebar.page_link("pages/weekly_report.py", label="Weekly Report", icon="👋")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg', 'webp', 'heic'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=False)
    
    # Classify  the image
    category = 'TEMP' #classify_image(image)          
    image_path = os.path.join(uploads_dir, uploaded_file.name)
    st.success(f'Classification : {category}')
    
    # Text box for comments
    comment = st.text_input("Add a comment about the image:")

    if st.button('Submit Comment'):
        # Get the timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Get and save the user's location
        #latitude, longitude = get_user_location()
        longitude = "long:000"
        latitude = "lat:000"
        st.write(f"Your location is: Latitude: {latitude}, Longitude: {longitude}")
        
        if comment:
            # Remove all commas from the comment
            sanitized_comment = comment.replace(',', '')
            # Save the uploaded file
            image_path = save_uploaded_file(image)

            # Append the new metadata to session state
            st.session_state.tracker.append({
                "image_path": image_path,
                "classification": classification,
                "timestamp": timestamp,
                "latitude": latitude,
                "longitude": longitude,
                "comment": sanitized_comment
            })
            st.success('Thanks for reporting your thoughts, we will look into it.')
        else:
            st.error('Please add a comment before submitting.')



    # Save the updated metadata to the tracker file
    with open(JSON_FILE, "w") as f:
        json.dump(st.session_state.metadata, f, indent=4)
        
    

# Run Streamlit app using 'streamlit run app.py' command
