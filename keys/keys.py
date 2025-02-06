import os
from dotenv import load_dotenv

#* Get environment
load_dotenv(".env")
environment = os.getenv("ENVIRONMENT", "development")  # Default to 'development'

#* laod proper environment file
dotenv_file = f".env.{environment}"
load_dotenv(dotenv_file)

#! Server URLs -----------------------------------------------
#* MongoDB Connection ----------------------------------------
mongo_uri = os.getenv("MONGO_URI")

#* Service URLs ---------------------------------------------
aiml_service_url = os.getenv("AIML_SERVICE_URL", "http://localhost:8000")

#! Keys -----------------------------------------------------
#* Aws keys -------------------------------------------------
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET")

#* Clerk keys -----------------------------------------------
clerk_secret_key = os.getenv("CLERK_SECRET_KEY")
jwks_json = os.getenv("JWKS_JSON")
jwks_issuer = os.getenv("JWKS_ISSUER")
