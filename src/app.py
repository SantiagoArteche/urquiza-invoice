from flask import Flask
from login.routes import login_bp

app = Flask(__name__)
app.register_blueprint(login_bp)

@app.route("/")
def running():
    return "<p>The server is running</p>"

if __name__ == "__main__":
    app.run(debug=True)