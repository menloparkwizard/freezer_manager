from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from freezer_app.auth import login_required
from freezer_app.db import get_db

bp = Blueprint('freezer', __name__)


@bp.route('/')
def index():
	db = get_db()
	food = db.execute(
		'SELECT f.id, name, servings, location_id, chef_id, added'
		' FROM food f JOIN user u ON f.chef_id = u.id'
		' FROM food f JOIN freezer z ON f.location_id = z.id'
		' ORDER BY added ASC'
	).fetchall()

	return render_template('freezer/index.html', food=food)