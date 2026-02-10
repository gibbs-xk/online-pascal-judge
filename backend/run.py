import os
from flask import Flask
from api.runScript.main import run
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.register_blueprint(run)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("DEBUG", "0") == "1"
    app.run(debug=debug, port=port, use_reloader=False)
