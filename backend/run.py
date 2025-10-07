# backend/run.py
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # For Render deployment - use PORT environment variable
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host="0.0.0.0", port=port)