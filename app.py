from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file.filename == '':
        return 'No file selected'
    
    if file and allowed_file(file.filename):
        file.save(file.filename)
        return 'File uploaded successfully'
    else:
        return 'Invalid file format. Please select a CSV file.'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/cluster')
def cluster():
    return render_template('cluster.html')

@app.route('/preprocess', methods=['POST'])
def preprocess():
    file = request.files['file']
    # Lakukan pemrosesan data menggunakan kode yang sudah Anda siapkan di sini
    # ...

    # Mengembalikan tampilan atau respon yang sesuai setelah pemrosesan selesai
    return "Data preprocessing completed successfully."

@app.route('/saveddata')
def saveddata():
    return render_template('saved_data.html')

if __name__ == '__main__':
    app.run(debug=True)
