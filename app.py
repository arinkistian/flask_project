from flask import Flask, render_template, request, redirect

import pandas as pd
from preprocess import preprocess_data
from clustering import perform_clustering

app = Flask(__name__)

preprocessed_data = pd.DataFrame()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/')
def index():
    return render_template('dashboard.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

@app.route('/cluster', methods=['GET'])
def cluster_data():
    global preprocessed_data
    # Perform clustering on the preprocessed data
    n_clusters = 4  # Set the desired number of clusters
    clusters = perform_clustering(preprocessed_data, n_clusters)

    # Render the cluster.html template and pass the clusters
    return render_template('cluster.html', clusters=clusters)


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
