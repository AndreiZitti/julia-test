from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import pandas as pd
import io
import os
from gender_classifier import classify_gender, classify_gender_with_ai

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/columns', methods=['POST'])
def get_columns():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Only Excel files are allowed'}), 400
        
        # Read the Excel file to get column names
        df = pd.read_excel(file)
        
        return jsonify({
            'success': True,
            'columns': list(df.columns),
            'total_rows': len(df)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error reading file: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        column_name = request.form.get('column_name')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not column_name:
            return jsonify({'error': 'Column name is required'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Only Excel files are allowed'}), 400
        
        # Read the Excel file
        df = pd.read_excel(file)
        
        # Check if column exists
        if column_name not in df.columns:
            return jsonify({
                'error': f'Column "{column_name}" not found. Available columns: {list(df.columns)}'
            }), 400
        
        # Get column preview for verification
        column_preview = df[column_name].head(10).tolist()
        
        return jsonify({
            'success': True,
            'columns': list(df.columns),
            'selected_column': column_name,
            'preview': column_preview,
            'total_rows': len(df)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/process', methods=['POST'])
def process_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        column_name = request.form.get('column_name')
        api_key = request.form.get('api_key', '').strip()
        use_ai = request.form.get('use_ai', 'false').lower() == 'true'
        
        if not file or not column_name:
            return jsonify({'error': 'File and column name are required'}), 400
        
        # Read the Excel file
        df = pd.read_excel(file)
        
        # Create a copy for processing
        result_df = df.copy()
        
        # Get unique names for processing
        names_to_process = df[column_name].tolist()
        
        # Process names using AI or rule-based approach
        if use_ai and api_key:
            # Process in batches for efficiency
            batch_size = 50
            all_results = {}
            ai_success = True
            ai_error_message = None
            model_used = None
            
            for i in range(0, len(names_to_process), batch_size):
                batch = names_to_process[i:i + batch_size]
                ai_response = classify_gender_with_ai(batch, api_key)
                
                if ai_response['success']:
                    all_results.update(ai_response['results'])
                    if not model_used:  # Store the model used from first successful batch
                        model_used = ai_response['model_used']
                else:
                    # AI failed - return error to frontend
                    return jsonify({
                        'success': False,
                        'error': f"AI Classification Failed: {ai_response['error']}"
                    }), 400
            
            # Map AI results back to the dataframe
            gender_results = []
            for name in names_to_process:
                if name in all_results:
                    gender_results.append(all_results[name])
                else:
                    gender_results.append('?')
            
            classification_method = f"AI ({model_used})"
        else:
            # Use rule-based classification
            gender_results = []
            for name in names_to_process:
                if pd.isna(name) or str(name).strip() == '':
                    gender_code = '?'
                else:
                    gender_code = classify_gender(str(name).strip())
                gender_results.append(gender_code)
            classification_method = "Rule-based"
        
        # Replace the column with gender codes
        result_df[column_name] = gender_results
        
        # Save the result to a temporary file
        output_filename = f"processed_{file.filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        result_df.to_excel(output_path, index=False)
        
        # Count the results
        counts = pd.Series(gender_results).value_counts().to_dict()
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'counts': counts,
            'total_processed': len(gender_results),
            'classification_method': classification_method
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 