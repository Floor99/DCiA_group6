################################# IMPORT PACKAGES ################################

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

################################# MAIN CODE ################################

app = Flask(__name__)
UPLOAD_FOLDER = 'dcia/static/data'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    Parameters:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has an allowed extension (either xlsx or csv), False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'csv'}

@app.route('/upload_files', methods=['POST'])
def upload_files():
    """
    Handle file uploads from the HTML form. 
    Save the files to dcia/static/data folder if they have allowed extensions.

    Returns:
        redirect: Redirects to the grant applications page after processing files.
    """
    # Define the keys that match the file inputs in your HTML form
    file_keys = ['attributes_file', 'grants_file', 'people_file']

    # Iterate over each expected file key
    for file_key in file_keys:
        # Check if the file was provided
        if file_key in request.files and request.files[file_key].filename != '':
            file = request.files[file_key]
            # Check if the file has an allowed extension
            if file and allowed_file(file.filename):
                # Secure the file name and save the file in the dcia/static/data folder
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                 # Return an error message if the file is not allowed
                return f"Error with {file_key}: File not allowed or missing"
        else:
            # If the file wasn't provided, skip it and use the existing one
            print(f"No file provided for {file_key}, using existing file.")

    return redirect(url_for('grant_applications'))


@app.route("/")
def index():
    """ Render the main index page. """
    return render_template('index.html')

@app.route('/sign_in')
def sign_in():
    """ Render the sign in page. """
    return render_template('sign_in.html')

@app.route('/grant_applications')
def grant_applications():
    """ Render the grant applications page. """
    return render_template('grant_applications.html')

@app.route('/co_authorship')
def co_authorship():
    """ Render the co-authorship page. """
    return render_template('co_authorship.html')

@app.route('/knowledge_sharing')
def knowledge_sharing():
    """ Render the knowledge sharing page. """
    return render_template('knowledge_sharing.html')

@app.route('/Mission')
def mission():
    """ Render the mission page. """
    return render_template('mission.html')

@app.route('/Team')
def team():
    """ Render our team page. """
    return render_template('team.html')

@app.route('/Product')
def product():
    """ Render the product page. """
    return render_template('product.html')

@app.route('/Documentation')
def documentation():
    """ Render the documentation page. """
    return render_template('documentation.html')

@app.route('/about')
def about():
    """ Render the about us page. """
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    """ Render the pricing page. """
    return render_template('pricing.html')

@app.route('/faqs')
def faqs():
    """ Render the FAQs page. """
    return render_template('faqs.html')

@app.route('/contact')
def contact():
    """ Render the contact page. """
    return render_template('contact.html')

@app.route('/grant_applications_expansion')
def grant_applications_expansion():
    """ Render the grant applications expansion page. """
    return render_template('grant_applications_expansion.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)