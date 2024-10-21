from controllers.people_controller import people
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)
app.register_blueprint(people, url_prefix="/people")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
