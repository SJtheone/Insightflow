from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

def calculate_insights(df):
    # (Esta função não foi alterada)
    insights = {}
    insights['total_sales'] = df['Sales'].sum()
    insights['total_expenses'] = df['Expenses'].sum()
    insights['profit'] = insights['total_sales'] - insights['total_expenses']

    if 'Product' in df.columns:
        insights['best_selling_product'] = df.groupby('Product')['Sales'].sum().idxmax()
    else:
        insights['best_selling_product'] = None

    insights['average_sales'] = df['Sales'].mean()
    insights['average_expenses'] = df['Expenses'].mean()

    insights['sales_to_expense_ratio'] = (insights['total_sales'] / insights['total_expenses']) if insights['total_expenses'] != 0 else np.nan

    return insights

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        df = pd.read_csv(file)

        required_columns = ['Sales', 'Expenses']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({"error": f"Missing required column: {col}"}), 400
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                return jsonify({"error": f"Column '{col}' must contain numeric values"}), 400

        insights = calculate_insights(df)

        cleaned_insights = {}
        for key, value in insights.items():
            if pd.isna(value):
                cleaned_insights[key] = None
            elif isinstance(value, (np.int64, np.int32)):
                cleaned_insights[key] = int(value)
            elif isinstance(value, (np.float64, np.float32)):
                cleaned_insights[key] = float(value)
            else:
                cleaned_insights[key] = value

        return jsonify(cleaned_insights)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.form.to_dict()
    # Aqui vais processar os dados recebidos (data)
    # Por exemplo, guardar numa base de dados ou num ficheiro
    print(data) # Imprime os dados na consola para ver o que está a ser enviado
    return jsonify({"success": True}) # Responde com sucesso
