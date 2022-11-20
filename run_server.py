from flask import Flask
from routes import url_path
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(url_path)

app_port = 8080

if __name__=="__main__":
    app.run(debug=True, port=app_port)