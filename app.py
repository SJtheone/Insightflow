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
    insights['sales_to_expense_ratio'] = (insights['total_sales'] / insights['total_expenses']) if insights['total_expenses'] != 0 else np.nan

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
        return jsonify(insights)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# HTML template for file upload
@app.route('/upload.html')
def upload_html():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload CSV</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f4f4f9;
            }
            .upload-container {
                text-align: center;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            input[type="file"] {
                margin: 20px 0;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-transform: uppercase;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="upload-container">
            <h1>Upload CSV File</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".csv" required>
                <br>
                <button type="submit">Upload</button>
            </form>
        </div>
    </body>
    </html>
    '''
