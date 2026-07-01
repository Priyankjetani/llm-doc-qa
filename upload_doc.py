from google.cloud import storage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def upload_file(bucket_name, source_file, dest_name):
    """
    Uploads a file to a GCP Cloud Storage bucket.
    
    bucket_name: name of your GCS bucket
    source_file: path to the file on your computer
    dest_name: what to name it inside the bucket
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(dest_name)
    blob.upload_from_filename(source_file)
    print(f"✅ Uploaded {source_file} to gs://{bucket_name}/{dest_name}")

if __name__ == "__main__":
    bucket_name = os.getenv("GCP_BUCKET")
    
    upload_file(
        bucket_name=bucket_name,
        source_file="mydoc.pdf",
        dest_name="docs/mydoc.pdf"
    )