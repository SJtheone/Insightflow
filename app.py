from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# ... (função calculate_insights)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # ... (código anterior para processar o ficheiro)

@app.route('/save_data', methods=['POST'])
def save_data():  # Definição da função
    try:        # <--- INDENTADO (4 espaços)
        data = request.form.to_dict()
        data = {k: [v] for k, v in data.items()}
        df = pd.DataFrame(data)

        # Determinar o caminho para guardar o ficheiro (consideração de segurança)
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, 'saved_data.csv') #nome do ficheiro

        df.to_csv(file_path, index=False)
        return jsonify({"success": True})
    except Exception as e: # <--- INDENTADO (4 espaços)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
