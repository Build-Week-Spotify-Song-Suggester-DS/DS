
'''stolen from ryans twitoff code refit'''

def create_app():

    app = Flask(__name__)

    # configuration variable to our app
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect our database to the app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        # query for all users in the database
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route("/reset")
    def reset():
        return 
    



    