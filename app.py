from flask import Flask, render_template, request, redirect

import pandas as pd
from preprocess import preprocess_data

# import pandas as pd

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/cluster')
def cluster():
    return render_template('cluster.html')

@app.route('/preprocess', methods=['POST'])
def preprocess_route():
    global preprocessed_data

    file = request.files['file']

    if file.filename == '':
        return 'No file selected'
    
    if file and allowed_file(file.filename):
        # Read the CSV file as DataFrame
        df_ = pd.read_csv(file)

        # Perform the preprocessing steps
        preprocessed_df = preprocess_data(df_)
        
        # Store the preprocessed data in a global variable
        global preprocessed_data
        preprocessed_data = preprocessed_df

        # Return the preprocessed data or appropriate response
        return redirect('/process_data')
        # return "Data preprocessing completed successfully."
    else:
        return 'Invalid file format. Please select a CSV file.'

@app.route('/result')
def result():
    global preprocessed_data
    return preprocessed_data.to_html()

@app.route('/process_data')
def process_data():
    # Access the preprocessed data through the global variable
    global preprocessed_data

    # Convert the preprocessed data to HTML format
    preprocessed_data_html = preprocessed_data.to_html()

    # Render the process_data.html template and pass the preprocessed data
    return render_template('process_data.html', data=preprocessed_data_html)

@app.route('/saveddata')
def saveddata():
    return render_template('saved_data.html')

if __name__ == '__main__':
    app.run(debug=True)
