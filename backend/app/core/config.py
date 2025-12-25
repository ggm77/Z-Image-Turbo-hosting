import os

class Settings:
    PROJECT_NAME: str = "Z-Image-Turbo Hosting"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH: str = os.path.join(BASE_DIR, "db", "app.db")
    IMG_DIR: str = os.path.join(BASE_DIR, "generated_images")

settings = Settings()

os.makedirs(settings.IMG_DIR, exist_ok=True)