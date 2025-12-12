import os
from dotenv import load_dotenv

env_path = os.path.abspath('.env')
print("ABS PATH =", env_path)

load_dotenv(env_path)

print("MONGO_URI:", os.getenv("MONGO_URI"))
