import os
from dotenv import load_dotenv
from app import create_app

dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
    
app = create_app()

if __name__=="__main__":
    app.run(host="localhost", port=8080)