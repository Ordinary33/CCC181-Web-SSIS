from flask import Flask
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/test")
def test():
    return "Testing"
 
if __name__ == "__main__":
    app.run(debug=True)
                    