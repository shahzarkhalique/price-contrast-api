# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_wNTU4WiDqJQ5@ep-square-tooth-a1szbuny-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
