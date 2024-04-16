from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'dcia/static/data'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'csv'}

@app.route('/upload_files', methods=['POST'])
def upload_files():
    # Define the keys that match the file inputs in your HTML form
    file_keys = ['attributes_file', 'grants_file', 'people_file']

    # Iterate over each expected file key
    for file_key in file_keys:
        # Check if the file was provided
        if file_key in request.files and request.files[file_key].filename != '':
            file = request.files[file_key]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return f"Error with {file_key}: File not allowed or missing"
        else:
            # If the file wasn't provided, skip it and use the existing one
            print(f"No file provided for {file_key}, using existing file.")

    return redirect(url_for('grant_applications'))



@app.route("/")
def index():
    return render_template('index.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/grant_applications')
def grant_applications():
    return render_template('grant_applications.html')

@app.route('/co_authorship')
def co_authorship():
    return render_template('co_authorship.html')

@app.route('/knowledge_sharing')
def knowledge_sharing():
    return render_template('knowledge_sharing.html')

@app.route('/Mission')
def mission():
    return render_template('mission.html')

@app.route('/Team')
def team():
    return render_template('team.html')

@app.route('/Product')
def product():
    return render_template('product.html')

@app.route('/Documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# @app.route('/dash/')
# def dash():
#     return render_template('dash.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
