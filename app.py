from flask import Flask, render_template, request, redirect, send_file, make_response
import pandas as pd
from io import BytesIO

from preprocess import preprocess_data
from clustering import perform_clustering

app = Flask(__name__)

preprocessed_data = pd.DataFrame()
merged_df = pd.DataFrame()

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
    global preprocessed_data, data_lrfm, merged_df  

    n_clusters = 3 

    cluster_counts, df_clustered = perform_clustering(preprocessed_data, n_clusters)

    # Merge data_lrfm with df_clustered based on the index
    merged_df = data_lrfm.merge(df_clustered[['Cluster']], left_index=True, right_index=True)

    merged_df['buyer_id'] = range(1, len(merged_df) + 1)
    # Move the "buyer_id" column to the left side
    cols = merged_df.columns.tolist()
    cols = ['buyer_id'] + [col for col in cols if col != 'buyer_id']
    merged_df = merged_df[cols]

    return render_template('cluster.html', clusters=cluster_counts, data_lrfm=merged_df)

@app.route('/download_merged_df', methods=['GET','POST'])
def download_merged_df():
    global merged_df

    file_format = request.form['file_format']

    if merged_df.empty:  # Check if merged_df is empty
        return redirect('/cluster')  # Redirect to the appropriate page

    if request.method == 'POST':
        file_format = request.form['file_format']

        # Create an in-memory file object
        output = BytesIO()

        # Export the merged_df DataFrame based on the selected file format
        if file_format == 'csv':
            merged_df.to_csv(output, index=False, encoding='utf-8-sig')
            file_extension = 'csv'
        elif file_format == 'excel':
            merged_df.to_excel(output, index=False)
            file_extension = 'xlsx'
        else:
            return 'Invalid file format.'

        output.seek(0)  # Move the file object's position to the beginning

        # Create a response with the file data
        response = make_response(output.getvalue())

        # Set the appropriate Content-Type and Content-Disposition headers
        response.headers['Content-Type'] = 'text/csv' if file_extension == 'csv' else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename=merged_df.{file_extension}'

        return response

    return redirect('/cluster')

@app.route('/download_cluster', methods=['GET'])
def download_cluster():
    return render_template('download_cluster.html')


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
