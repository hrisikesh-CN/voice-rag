import re
import sys
import subprocess
import shutil
import os

def extract_s3_info(url):
    # Define the regex pattern for extracting bucket name and filename
    pattern = r"https://([^.]+)\.s3\.amazonaws\.com/(.+)"
    match = re.match(pattern, url)
    if match:
        bucket_name = match.group(1)
        filename = match.group(2)
        return bucket_name, filename
    else:
        raise ValueError("URL format is not valid")





def delete_folder(folder_path):
    """
    Deletes the specified folder and all its contents.
    
    Args:
        folder_path (str): The path to the folder to delete.
    """
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove the folder and its contents
        shutil.rmtree(folder_path)
        print(f"Deleted {folder_path} and all its contents.")
    else:
        print(f"{folder_path} does not exist.")


