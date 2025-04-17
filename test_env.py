import os
from dotenv import load_dotenv

load_dotenv(override=True)

print("DATABASE_HOST:", os.getenv("DATABASE_HOST"))
print("DATABASE_PASSWORD:", os.getenv("DATABASE_PASSWORD"))