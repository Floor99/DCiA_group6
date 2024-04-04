import subprocess
import concurrent.futures

#run this app to run both the graph and the website

def run_flask_app(file_name, port):
    subprocess.run(['python', file_name, '--port', str(port)])

if __name__ == '__main__':
    # Specify the file names and ports for each Flask application
    apps = [
        ('dcia/construct_graph.py', 5001),
        ('dcia/app.py', 5000)
    ]

    # Run each Flask application in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: run_flask_app(*x), apps)