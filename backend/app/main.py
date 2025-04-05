# EmployeeReviewByAi/backend/app/main.py
from flask import Flask
from routes import api
from gpt_api import gpt_api

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(gpt_api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)