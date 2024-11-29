import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_postgres_uri():
    # host = os.environ.get("DATABASE_URL", "localhost")
    # port = 54321 if host == "localhost" else 5432
    # password = os.environ.get("DB_PASSWORD", "abc123")
    # user, db_name = "allocation", "allocation"
    db_url = os.getenv("DATABASE_URL")

    return db_url


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"