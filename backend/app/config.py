import os
from pathlib import Path
from dotenv import load_dotenv

# Locate the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load environment variables from the root .env file
load_dotenv(PROJECT_ROOT / ".env")

# JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is missing from the .env file")