from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def calculate_insights(df):
    insights = {}
    insights['total_sales'] = df['Sales'].sum() if 'Sales' in df else None #Tratamento para quando a coluna nao existe
    insights['total_expenses'] = df['Expenses'].sum() if 'Expenses' in df else None
    if insights['total_expenses'] != 0 and insights['total_expenses'] is not None:
      insights['sales_to_expense_ratio'] = (insights['total_sales'] / insights['total_expenses'])
    else:
      insights['sales_to_expense_ratio'] = None
    insights['profit'] = insights['total_sales'] - insights['total_expenses'] if insights['total_sales'] is not None and insights['total_expenses'] is not None else None
    if 'Product' in df.columns:
        insights['best_selling_product'] = df.groupby('Product')['Sales'].sum().idxmax()
    else:
        insights['best_selling_product'] = None
    insights['average_sales'] = df['Sales'].mean() if 'Sales' in df else None
    insights['average_expenses'] = df['Expenses'].mean() if 'Expenses' in df else None
    return insights

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
                    df[col] = pd.to_numeric(df[col], errors='coerce') #Trata erros de conversao para numeros e mete NaN
                except ValueError:
                    return jsonify({"error": f"A coluna '{col}' deve conter valores numéricos"}), 400
            df.dropna(inplace=True) #Remove linhas com NaN
            if df.empty: #verifica se o dataframe esta vazio depois de remover os NaN
                return jsonify({"error": "O ficheiro não tem dados válidos para processar."})
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
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
