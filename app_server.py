from app import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# This code is the entry point for the Flask application.
# It imports the app from app.py and runs it on the specified port.
# The port defaults to 5000 if not set in the environment variables.
# The app will be accessible from any IP address