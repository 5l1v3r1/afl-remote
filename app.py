from flask import Flask, render_template, request
from database import get_db, close_db
from user import user_pages
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return "Sup!"

@app.teardown_appcontext
def close_application(error):
    close_db()

app.register_blueprint(user_pages, url_prefix='/user')

if __name__ == "__main__":
    app.secret_key = 'FKLDSJDLKSFJALSKDJ:AK' # TODO make random in config
    app.run(debug=True)
