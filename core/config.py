from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION   = os.getenv("GCP_LOCATION")
GCP_BUCKET     = os.getenv("GCP_BUCKET")