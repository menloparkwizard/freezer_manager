import os
from flask import Flask

def create_app(test_config=None):
	# Create and Configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'freezer_manager.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# Ensure that the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Create a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello freezer world!'
	
	# Register the database
	from . import db
	db.init_app(app)

	# Regster the Authentication Module
	from . import auth
	app.register_blueprint(auth.bp)

	# Register the Freezer Module
	from . import freezer
	app.register_blueprint(freezer.bp)
	app.add_url_rule('/', endpoint='index')
	
	return app