from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, Marijn!</p>"

if __name__ == "__main__":
    app.run()


# app.py contains your Flask application code, including route definitions, database connections, and any other application setup.
