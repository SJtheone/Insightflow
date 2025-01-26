from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Configuração para a pasta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) # Cria a pasta se não existir

def calculate_insights(df):
    # ... (mesma função calculate_insights das respostas anteriores)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum ficheiro selecionado"})

        file = request.files['file']

        try:
            df = pd.read_csv(file)
            required_columns = ['Sales', 'Expenses']
            for col in required_columns:
                if col not in df.columns:
                    return jsonify({"error": f"Falta a coluna obrigatória: {col}"}), 400
                try:
                    df[col] = pd.to_numeric(df[col])
                except ValueError:
                    return jsonify({"error": f"A coluna '{col}' deve conter valores numéricos"}), 400
            insights = calculate_insights(df)
            return jsonify(insights)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('upload.html')

@app.route('/save_data', methods=['POST'])
def save_data():
    try:
        data = request.form.to_dict()
        data = {k: [v] for k, v in data.items()}
        df = pd.DataFrame(data)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_data.csv')
        df.to_csv(file_path, index=False)
        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<path:filename>')
def download_file(filename): #Nova rota para downloads
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
