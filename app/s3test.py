"""

Example of an S3 object:

Bucket: my-bucket
Object Key: my-folder/my-file.txt
Data: The content of the file "my-file.txt"
Metadata: Information like last modified date, content type, custom tags, etc.

"""

import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def upload_to_s3(file_name, bucket, folder_name, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    object_key = f"{folder_name}/{object_name}"
    
    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # Upload the file
        s3_client.upload_file(file_name, bucket, object_key)
        print(f"File {file_name} uploaded to {bucket}/{object_key}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return False

# Replace these values with your file path, bucket name, and desired object name in S3
file_name = 'uploads/0a86f0ba-47f8-40fd-b5c2-3646a294bf4d_thumb.jpg'
bucket_name = 'broken-windows'
folder_name = 'uploadstest'
object_name = '0a86f0ba-47f8-40fd-b5c2-3646a294bf4d_thumb.jpg'  # Optional

# Call the function to upload the file
#upload_to_s3(file_name, bucket_name, folder_name, object_name)





def upload_directory_to_s3(directory_path, bucket_name, s3_prefix=''):
    """
    Uploads a directory of files to an S3 bucket.

    :param directory_path: Path to the local directory to upload
    :param bucket_name: Name of the S3 bucket
    :param s3_prefix: Optional prefix for the S3 object keys (simulates folder structure in S3)
    """
    s3_client = boto3.client('s3')
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, directory_path)
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")
            
            try:
                s3_client.upload_file(local_path, bucket_name, s3_path)
                print(f"File {local_path} uploaded to {bucket_name}/{s3_path}")
            except FileNotFoundError:
                print(f"The file {local_path} was not found.")
            except NoCredentialsError:
                print("Credentials not available.")
            except PartialCredentialsError:
                print("Incomplete credentials provided.")
            except Exception as e:
                print(f"Failed to upload {local_path} to {bucket_name}/{s3_path}. Error: {e}")

# Streamlit secrets to get the S3 bucket name
s3_bucket = bucket_name

# Specify the local directory you want to upload
local_directory = 'sample_data'

# Optional: specify a prefix to use as a "folder" in S3
s3_prefix = 'sample_data'

# Call the function to upload the directory
upload_directory_to_s3(local_directory, s3_bucket, s3_prefix)