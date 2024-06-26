import threading
from flask import render_template, request, jsonify
from flask.cli import AppGroup
from __init__ import app, db, cors
from api.user import user_api
from api.player import player_api
from api.titanic import titanic_api
from api.food import food_api
from api.bakery import bakery_api
from api.stock import stocks_api
from api.house_price import house_price_api
# database migrations
from model.users import initUsers
from model.players import initPlayers
from model.bakings import initBakings

# setup APIs from first file
from api.covid import covid_api
from api.joke import joke_api

# setup App pages from second file
from projects.projects import app_projects

# database migrations from second file
from model.foods import initfood
from model.bakeries import initbakery
from api.titanic import titanic_api
from api.food import food_api
from api.bakery import bakery_api
from api.baking import baking_api

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# register URIs from both files
app.register_blueprint(user_api)
app.register_blueprint(player_api)
app.register_blueprint(covid_api)
app.register_blueprint(joke_api)
app.register_blueprint(titanic_api)
app.register_blueprint(food_api)
app.register_blueprint(stocks_api)
app.register_blueprint(bakery_api)
app.register_blueprint(house_price_api)
app.register_blueprint(baking_api)
app.register_blueprint(app_projects)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

@app.route('/settings/')
def settings():
    return render_template("settings.html")

@app.route('/api/users/save_settings', methods=['POST'])
def save_settings():
    try:
        settings = request.json.get('settings')

        return jsonify({'message': 'Settings saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.before_request
def before_request():
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://tuckergol.github.io/frontgang/']:
        cors._origins = allowed_origin

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()
    initBakings()
    initfood()
    initbakery()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
# @app.before_first_request
def activate_job():
    initUsers()
    initBakings()

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8008")
