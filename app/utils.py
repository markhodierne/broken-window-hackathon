"""
Utility functions for the 'I Love My Neighbourhood' App.

These functions handle file operations for both local and cloud environments.
"""

import random
import os
import uuid
import base64
import shutil
from io import StringIO, BytesIO

import streamlit as st
import boto3
import requests
import pandas as pd
from PIL import Image


def check_file_exists_on_s3(s3_client: boto3.client, 
        bucket: str, key: str) -> bool:
    """
    Check if a file exists on S3.

    Args:
        s3_client (boto3.client): The S3 client.
        bucket (str): The name of the S3 bucket.
        key (str): The key of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except Exception as e:
        st.write(f"An unexpected error occurred: {e}")
        return False


def load_tracker_data(tracker_file, cloud, s3_client=None, s3_bucket=None):
    """
    Load the tracker data from a CSV file.

    Args:
        tracker_file (str): Path to the tracker file.
        cloud (bool): Indicates if the deployment is cloud-based.
        s3_client (boto3.client, optional): The S3 client.
        s3_bucket (str, optional): The S3 bucket name.

    Returns:
        pd.DataFrame: The loaded tracker data.
    """
    if cloud:
        try:
            response = s3_client.get_object(Bucket=s3_bucket, Key=tracker_file)
            csv_content = response['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            return df
        except Exception as e:
            st.write(f"Failed to read CSV from S3. Reason: {e}")
            return None
    else:
        try:
            df = pd.read_csv(tracker_file)
            return df
        except Exception as e:
            st.write(f"Failed to read CSV locally. Reason: {e}")
            return None
    
    
def get_base64(file_path, cloud, s3_client=None, s3_bucket=None):
    """
    Download image from local or S3 and convert it to base64.

    Args:
        file_path (str): The path to the image file.
        cloud (bool): Whether the deployment is cloud-based.
        s3_client (boto3.client, optional): The S3 client.
        s3_bucket (str, optional): The S3 bucket name.

    Returns:
        str: The base64 encoded string of the image.
    """
    if cloud:
        try:
            response = s3_client.get_object(Bucket=s3_bucket, Key=file_path)
            image = response['Body'].read()
            return base64.b64encode(image).decode()
        except Exception as e:
            st.write(f"Failed to read image from S3. Reason: {e}")
            return None
    else:
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()


def query(payload, api_url, headers):
    """
    Send a POST request to the Hugging Face API with the given payload.

    Args:
        payload (dict): The payload to send in the POST request.
        api_url (str): The API URL.
        headers (dict): The headers for the request.

    Returns:
        dict: The response from the API.
    """
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()


def get_location():
    """
    Function to get user's location based browser geolocation. This function 
    is not implemented - instead, a random location is assigned within an area 
    of South East London.

    Returns:
        tuple: A tuple containing latitude and longitude.
    """
    latitude = round(random.uniform(51.466, 51.478), 3)
    longitude = round(random.uniform(-0.081, -0.056), 3)  
    return latitude, longitude


def save_uploaded_file(uploaded_file, uploads_dir, cloud, 
        s3_client=None, s3_bucket=None):
    """
    Save the uploaded file and return the file path.

    Args:
        uploaded_file (UploadedFile): The uploaded file.
        cloud (bool): Whether the deployment is cloud-based.
        s3_client (boto3.client): The S3 client.
        s3_bucket (str): The S3 bucket name.
        uploads_dir (str): The uploads directory.

    Returns:
        tuple: A tuple containing the file name and the resized image.
    """
    file_id = str(uuid.uuid4())
    file_extension = uploaded_file.name.split(".")[-1]
    file_name = f"{file_id}.{file_extension}"
    
    uploaded_file_copy = BytesIO(uploaded_file.read())
    image = Image.open(uploaded_file_copy)

    smallest_dimension = 300
    original_width, original_height = image.size
    
    if original_width < original_height:
        new_width = smallest_dimension
        new_height = int((smallest_dimension / original_width) * original_height)
    else:
        new_height = smallest_dimension
        new_width = int((smallest_dimension / original_height) * original_width)
        
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    if cloud:
        resized_buffer = BytesIO()
        resized_image.save(resized_buffer, format=image.format)
        resized_buffer.seek(0)
        file_path = os.path.join(uploads_dir, file_name)
        s3_client.put_object(
            Bucket=s3_bucket, 
            Key=file_path, 
            Body=resized_buffer
        )
    else:
        resized_buffer = BytesIO()
        resized_image.save(resized_buffer, format=image.format)
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(resized_buffer.getvalue())
        
    return file_name, resized_image


def save_image_data(image_path, classification, timestamp, latitude, longitude, 
        comment, tracker_file, cloud, s3_client=None, s3_bucket=None):
    """
    Save image data to the tracker file.

    Args:
        image_path (str): The path of the image.
        classification (str): The classification of the image.
        timestamp (str): The timestamp of the image.
        latitude (float): The latitude of the image location.
        longitude (float): The longitude of the image location.
        comment (str): The comment about the image.
        cloud (bool): Whether the deployment is cloud-based.
        s3_client (boto3.client): The S3 client.
        s3_bucket (str): The S3 bucket name.
        tracker_file (str): The tracker file path.
    """
    data = [
        image_path, classification, timestamp, latitude, longitude, comment
    ]
    
    if cloud:
        try:
            response = s3_client.get_object(Bucket=s3_bucket, Key=tracker_file)
            csv_content = response['Body'].read().decode('utf-8')
            if not csv_content.endswith('\n'):
                csv_content += '\n'
            updated_csv_content = csv_content + ",".join(map(str, data)) + "\n"
            s3_client.put_object(
                Bucket=s3_bucket, Key=tracker_file, Body=updated_csv_content
            )
        except Exception as e:
            st.write(f"Failed to append data to CSV on S3. Reason: {e}")
    else:
        try:
            with open(tracker_file, 'a+') as f:
                f.seek(0, os.SEEK_END)
                if f.tell() > 0:
                    f.seek(f.tell() - 1)
                    if f.read(1) != '\n':
                        f.write('\n')
                f.write(",".join(map(str, data)) + "\n")
        except Exception as e:
            st.write(f"Failed to append data to CSV locally. Reason: {e}")


def delete_dir(dir_name, cloud, s3_client=None, s3_bucket=None):
    """
    Delete all files in the specified directory, either locally or in S3.

    Args:
        dir_name (str): The name of the directory to delete.
        cloud (bool): Whether the deployment is cloud-based.
        s3_client (boto3.client): The S3 client.
        s3_bucket (str): The S3 bucket name.
    """
    if cloud:
        try:
            response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=dir_name)
            if 'Contents' in response:
                for item in response['Contents']:
                    s3_client.delete_object(Bucket=s3_bucket, Key=item['Key'])
                st.write(f'All reports have been deleted successfully.')
        except Exception as e:
            st.write(f"Failed to delete all reports. Reason: {e}")
    else:
        try:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                st.write('All reports have been deleted successfully.')
        except Exception as e:
            st.write(f"Failed to delete all reports. Reason: {e}")


def add_sample_data(source_dir, target_dir, cloud, s3_client=None, 
        s3_bucket=None):
    """
    Add sample data to the specified directory, either locally or in S3.

    Args:
        source_dir (str): The source directory containing sample data.
        target_dir (str): The target directory where sample data will be copied.
        cloud (bool): Whether the deployment is cloud-based.
        s3_client (boto3.client): The S3 client.
        s3_bucket (str): The S3 bucket name.
    """
    if cloud:
        try:
            response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=source_dir)
            if 'Contents' not in response:
                st.write(f"No sample data found at {source_dir}.")
                return

            for obj in response['Contents']:
                source_key = obj['Key']
                new_key = target_dir + source_key[len(source_dir):]
                copy_source = {'Bucket': s3_bucket, 'Key': source_key}
                s3_client.copy_object(CopySource=copy_source, Bucket=s3_bucket, Key=new_key)
            st.write('Sample reports have been loaded successfully.')
        except Exception as e:
            st.write(f"Failed to create sample reports. Reason: {e}")
    else:
        try:
            if os.path.exists(source_dir) and os.path.isdir(source_dir):
                shutil.copytree(source_dir, target_dir)
                st.write('Sample reports have been loaded successfully.')
        except Exception as e:
            st.write(f"Failed to create sample reports. Reason: {e}")
