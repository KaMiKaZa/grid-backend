from flask import Flask
from blueprints import database


app = Flask(__name__)
app.register_blueprint(database.bp)


if __name__ == '__main__':
    app.run()