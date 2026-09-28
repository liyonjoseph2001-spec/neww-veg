from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# VERCEL FIX: Vercel serverless functions are read-only except for the /tmp directory.
# If you try to save to a standard 'uploads' folder, Vercel will throw an Error 500.
UPLOAD_FOLDER = '/tmp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Serves the index.html from the templates folder
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # =======================================================
        # ⚠️ AI MODEL INTEGRATION POINT ⚠️
        # Replace the dummy data below with your actual AI code.
        # =======================================================
        
        # Simulated AI response for demonstration
        mock_predictions = [
            {"name": "Apple", "confidence": 0.96, "type": "Fruit"},
            {"name": "Carrot", "confidence": 0.88, "type": "Vegetable"}
        ]
        
        # Delete the image after processing to keep /tmp clean
        if os.path.exists(filepath):
            os.remove(filepath)
            
        return jsonify(mock_predictions)

# Keep for local testing; Vercel ignores this block
if __name__ == '__main__':
    app.run(debug=True, port=5000)
