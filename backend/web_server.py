from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Path to frontend folder
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.route('/')
def index():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_PATH, filename)

@app.route('/health')
def health():
    return {"status": "Website server running", "port": 3000}

if __name__ == '__main__':
    print("🌐 Starting TechCorp Website Server...")
    print("📁 Serving files from:", os.path.abspath(FRONTEND_PATH))
    print("🔗 Website URL: http://localhost:3000")
    print("🔧 Make sure your frontend files are in the 'frontend' folder!")
    app.run(debug=True, port=3000, host='0.0.0.0')
