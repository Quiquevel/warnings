import uvicorn
from src.app.main import app

if __name__ == "__main__":
  uvicorn.run("asgi:app", host="0.0.0.0", port=8080 )
