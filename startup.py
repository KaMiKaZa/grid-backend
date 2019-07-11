from flask import Flask
from blueprints import database, hooks


app = Flask(__name__)
app.register_blueprint(database.bp)
app.register_blueprint(hooks.bp)


if __name__ == '__main__':
    app.run()