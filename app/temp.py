import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_token = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_token)

# Read the CSV file
df = pd.read_csv("uploads/tracker.csv")
print(df.head())