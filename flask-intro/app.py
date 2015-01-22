from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    hello = 'Hello World!'
    response = hello + 42  # fail
    return response


if __name__ == '__main__':
    app.run(debug=True)
