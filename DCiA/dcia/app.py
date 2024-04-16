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
    files = {
        'attributes_final.xlsx': request.files['attributes_file'],
        'grants_to_people.csv': request.files['grants_file'],
        'people_to_people.csv': request.files['people_file']
    }

    for file_name, file in files.items():
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        else:
            return f"Error with {file_name}: File not allowed or missing"

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
