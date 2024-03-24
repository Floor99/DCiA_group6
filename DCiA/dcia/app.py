from flask import Flask, render_template


app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)


# app.py contains your Flask application code, including route definitions, database connections, and any other application setup.
