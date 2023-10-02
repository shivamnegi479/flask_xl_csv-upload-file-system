from flask import Flask, render_template, request, send_file, redirect
import os
import pandas 



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ADMIN_USERNAME'] = 'admin'
app.config['ADMIN_PASSWORD'] = 'admin'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.files['file'].filename == '':
        return render_template('index.html',message="Please Select any csv or excel file")
    elif not request.files['file'].filename.endswith('csv') and not request.files['file'].filename.endswith('xlsx'):
        return render_template('index.html',message="Select Only Csv or Excel files")
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html',message="File Upload Succesfully")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            return render_template('admin.html', files=files)
        else:
            return render_template('login.html', message='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route("/show/<filename>")
def show(filename):
    if str(filename).endswith('csv') or str(filename).endswith('xlsx'):
        try:
            file = pandas.read_excel(os.path.join(app.config['UPLOAD_FOLDER'])+"/"+filename)
            main_file=file

        except:    
            file2 = pandas.read_csv(os.path.join(app.config['UPLOAD_FOLDER'])+"/"+filename)
            main_file=file2
        main_file.to_html("templates/show.html") 

        return render_template("show.html")
    else:
        return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
