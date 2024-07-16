"""
Summary Reports page for 'I Love My Neighbourhood' App.

Functions:
- Load and display residents' reports from a tracker file.
- Summarize comments by category using OpenAI's GPT-3.5-Turbo model.
- Display the summarized reports and the original reports.

Data is stored locally for local deployment and on AWS S3 for 
Streamlit Cloud deployment.
"""

import streamlit as st
import pandas as pd
from openai import OpenAI

from utils import load_tracker_data


# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
api_token = st.session_state.openai_api_token
cloud = st.session_state.cloud

if cloud:
    s3_bucket = st.session_state.s3_bucket
    s3_client = st.session_state.s3_client
else:
    s3_bucket = None
    s3_client = None


# Initialize the client
client = OpenAI(api_key=api_token)


def summarize_comments(df):
    """
    Summarize comments by category using OpenAI's GPT-3.5-Turbo model.

    Args:
        df (pd.DataFrame): DataFrame containing the reports data.

    Returns:
        str: The summarized text of comments by category.
    """
    summaries = []
    feedback_counts = []
    categories = df['classification'].unique()
    for category in categories:
        df_category = df[df['classification'] == category]
        
        # Count number of feedbacks (images) in the category
        feedback_count = df_category.shape[0]
        feedback_counts.append((category, feedback_count))
        
        comments = " ".join(df_category['comment'].tolist())
        if comments:
            prompt = f"""
                Summarize the following comments from residents of the 
                neighbourhood. Do not use your memory of any previous 
                similar tasks. Only make use of the comments provided
                in this message when formulating your summary - do NOT
                make up information that is not contained within the 
                comments below.
                
                In one single paragraph of maximum length 300 words:

                1. Provide a brief overview of the main topics 
                discussed.
                2. Highlight the most significant concerns or issues, 
                if raised
                3. Mention any positive feedback or suggestions, 
                if raised.
                4. Summarize in a concise, clear manner, suitable for 
                community leaders and providers of public services.
                
                Do NOT make up any information that is not present in 
                the comments that follow.

                Here are the comments to summarize (use only these 
                comments as the input for your summarization):
                \n\n{comments}
                """
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.5
            )
            summary = response.choices[0].message.content.strip()
            summaries.append((category, summary))
    
    # Sort summaries based on feedback count from highest to lowest
    feedback_counts.sort(key=lambda x: x[1], reverse=True)
    
    summary_text = ""
    for category, count in feedback_counts:
        summary_text += f"**{category}** ({count} reports)<br>"
        summary_text += next(
            (summary for cat, summary in summaries if cat == category), 
            "No summary available") + "\n\n"
    return summary_text


# Load the tracker into a DataFrame
df = load_tracker_data(tracker_file, cloud, s3_client, s3_bucket) 
df.set_index('timestamp', inplace=True)  

st.markdown("""
    <div style='text-align: center;'>
        <h1>Summaries by Reporting Category</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

st.write(
    """
    Use the button below to produce an AI generated summary of 
    residents' reports.
    """, 
    unsafe_allow_html=True
)

# Summarize comments
if st.button('Summarize Reports'):
    summaries = summarize_comments(df)
    st.write("")
    st.markdown(summaries, unsafe_allow_html=True)

st.divider()

# Display the tracker DataFrame
st.markdown(
    """
    <div style='text-align: center;'>
        <h3> Residents' Reports </h3>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write(df)
