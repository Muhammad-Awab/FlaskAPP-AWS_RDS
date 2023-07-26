# app.py
from flask import Flask, render_template
from routes.user_routes import user_routes

app = Flask(__name__)

# Register the user_routes Blueprint
app.register_blueprint(user_routes)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
