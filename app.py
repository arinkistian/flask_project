from flask import Flask, render_template, request, redirect, send_file
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

@app.route('/preprocess', methods=['POST'])
def preprocess_route():
    global preprocessed_data, data_lrfm, df_scaled

    file = request.files['file']

    if file.filename == '':
        return 'No file selected. Upload Data'
    
    if file and allowed_file(file.filename):
        # Read the CSV file as DataFrame
        df_ = pd.read_csv(file)

        # Perform the preprocessing steps
        data_lrfm, df_scaled = preprocess_data(df_)
        
        # Store the preprocessed data in a global variable
        preprocessed_data = df_scaled
        
        return redirect('/process_data')
        # return "Data preprocessing completed successfully."
    else:
        return 'Invalid file format. Please select a CSV file.'

@app.route('/cluster', methods=['GET'])
def cluster_data():
    global preprocessed_data, data_lrfm

    n_clusters = 3 
    # clusters = perform_clustering(preprocessed_data, n_clusters, verbose=False)

    # data_lrfm_copy = data_lrfm.copy()
    # data_lrfm_copy['Cluster'] = clusters['Cluster']

    # print(data_lrfm_copy)

    cluster_counts, df_clustered = perform_clustering(preprocessed_data, n_clusters)

    # Merge data_lrfm with df_clustered based on the index
    merged_df = data_lrfm.merge(df_clustered[['Cluster']], left_index=True, right_index=True)

    # Merge data_lrfm with cluster_results based on the index
    # merged_df = data_lrfm_copy.merge(cluster_results, left_index=True, right_index=True)

    return render_template('cluster.html', clusters=cluster_counts, data_lrfm=merged_df)

@app.route('/process_data')
def process_data():
    # Access the preprocessed data through the global variable
    global preprocessed_data
    if preprocessed_data.empty:
        return redirect('/')

    # Convert the preprocessed data to HTML format
    preprocessed_data_html = preprocessed_data.to_html()

    # Render the process_data.html template and pass the preprocessed data
    return render_template('process_data.html', data=preprocessed_data_html)

@app.route('/saveddata')
def saveddata():
    return render_template('saved_data.html')

if __name__ == '__main__':
    app.run(debug=True)
