from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

# Route for the homepage


def calculate_insights(df):
    insights = {}

    # Total sales and expenses
    insights['total_sales'] = df['Sales'].sum()
    insights['total_expenses'] = df['Expenses'].sum()

    # Profit calculation
    insights['profit'] = insights['total_sales'] - insights['total_expenses']

    # Best selling product
    if 'Product' in df.columns:
        insights['best_selling_product'] = df.groupby('Product')['Sales'].sum().idxmax()

    # Average sales and expenses
    insights['average_sales'] = df['Sales'].mean()
    insights['average_expenses'] = df['Expenses'].mean()

    # Sales to expense ratio
    insights['sales_to_expense_ratio'] = (
        insights['total_sales'] / insights['total_expenses']
    ) if insights['total_expenses'] != 0 else np.nan

    return insights


@app.route('/')
def home():
    return render_template('upload.html')  # HTML file to upload the CSV


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file)

        # Validate required columns
        required_columns = ['Sales', 'Expenses']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({"error": f"Missing required column: {col}"}), 400

        # Calculate insights
        insights = calculate_insights(df)

        # Fix for JSON serialization error: convert int64 and float64 to int, float or None
        for key, value in insights.items():
            if isinstance(value, np.int64):
                insights[key] = int(value)
            elif isinstance(value, np.float64):
                insights[key] = float(value)
            elif pd.isna(value):
                insights[key] = None

        return jsonify(insights)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    # ... (código anterior)

    try:
        df = pd.read_csv(file)

        required_columns = ['Sales', 'Expenses']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({"error": f"Missing required column: {col}"}), 400
            try:
                df[col] = pd.to_numeric(df[col]) # Converter para números
            except ValueError:
                return jsonify({"error": f"Column '{col}' must contain numeric values"}), 400
        # ... (resto do código)
