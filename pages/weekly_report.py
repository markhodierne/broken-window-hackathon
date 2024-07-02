import streamlit as st


st.set_page_config(
        page_title="Weekly Report",
        page_icon="👋",
    )

st.title("Weekly Report 👋")
st.sidebar.page_link("pages/weekly_report.py", label="Weekly Report", icon="👋")

st.write("Click below to create this week's report for your neighbourhood.")
if st.button('Generate Report'):
    
    
    
# Set OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
openai.api_key = api_key
print("---------API_FOUND_AND_WORKS---------")

def summarize_comments(doc_text):
    prompt = f"Summarize the following user comments and address the major concerns mentioned:\n\n{doc_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000,
        temperature=0.5
    )
    return response.choices[0].message['content'].strip()

# Read the text file with user comments
with open("user_comments.txt", "r") as file:
    comments = file.read()

# Summarize the comments and address the major concerns
summary = summarize_comments(comments)

# Print or save the summary
print(summary)
with open("summary.txt", "w") as summary_file:
    summary_file.write(summary)
