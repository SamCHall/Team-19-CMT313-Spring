from flask import render_template

from .. import app

@app.errorhandler(400)
def bad_request(error):
    return render_template('errors.html', title="400 - Bad Request", error=error), 400

@app.errorhandler(401)
def unauthorized(error):
    return render_template('errors.html', title="401 - Unauthorized", error=error), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors.html', title="403 - Forbidden", error=error), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors.html', title="404 - Page not found", error=error), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('errors.html', title="405 - Method Not Allowed", error=error), 405

@app.errorhandler(500)
def not_implemented(error):
    return render_template('errors.html', title="500 - Internal Server Error", error=error), 500

@app.errorhandler(501)
def not_implemented(error):
    return render_template('errors.html', title="501 - Not implemented", error=error), 501
