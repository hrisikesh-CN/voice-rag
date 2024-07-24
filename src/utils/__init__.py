import re
import sys
import subprocess


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



