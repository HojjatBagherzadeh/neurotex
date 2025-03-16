import os

class Config:
    # Read environment variable or use default value
    LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "local")

config = Config()
