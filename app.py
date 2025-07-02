import os, uuid
from flask import Flask, request, send_from_directory, redirect, url_for, render_template

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Brak pliku", 400
        file = request.files['file']
        if file.filename == '':
            return "Nie wybrano pliku", 400
        uid = str(uuid.uuid4())
        fname = f"{uid}_{file.filename}"
        file.save(os.path.join(UPLOAD_FOLDER, fname))
        return redirect(url_for('download_link', filename=fname))
    return render_template('index.html')

@app.route('/download/<filename>')
def download_link(filename):
    return f'''
      <p>Plik przesłany!</p>
      <a href="/file/{filename}">Pobierz plik</a>
    '''

@app.route('/file/<filename>')
def serve_file(filename):
    return send_from_directory(
    app.config['UPLOAD_FOLDER'],
    filename,
    as_attachment=True,
    mimetype='video/mp4'
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)