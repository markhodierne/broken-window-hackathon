import streamlit as st
import pandas as pd
from openai import OpenAI


# Load the session state variables
uploads_dir = st.session_state.uploads_dir
tracker_file = st.session_state.tracker_file
api_token = st.session_state.openai_api_token

# Initialize the client
client = OpenAI(api_key=api_token)
	
# Load the tracker
df = pd.read_csv(tracker_file)
df.set_index('timestamp', inplace=True)


# Function to summarize comments
def summarize_comments(df):
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
                    Summarize the following comments from residents of the neighbourhood. 
                    In one single paragraph of maximum length 300 words:

                    1. Provide a brief overview of the main topics discussed.
                    2. Highlight the most significant concerns or issues, if raised
                    3. Mention any positive feedback or suggestions, if raised.
                    4. Summarize in a concise, clear manner, suitable for community leaders and providers of public services.

                    Here are the comments to summarize:\n\n{comments}
            """
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Make sure this is the correct model name
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
        summary_text += next((summary for cat, summary in summaries if cat == category), "No summary available") + "\n\n"

    return summary_text


st.markdown("""
<div style='text-align: center;'>
    <h1>Summaries by Reporting Category</h1>
</div>
""", unsafe_allow_html=True)

st.divider()

st.write("")
st.write("Use the button below to produce an AI generated summary of residents' reports.", unsafe_allow_html=True)

# Summarize comments
if st.button('Summarize Reports'):
    summaries = summarize_comments(df)
    st.write("")
    st.markdown(summaries, unsafe_allow_html=True)

st.divider()

# Display the DataFrame
st.markdown("""
<div style='text-align: center;'>
    <h3> Residents' Reports </h3>
</div>
""", unsafe_allow_html=True)
st.write(df)
