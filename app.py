"""Main web site flask app module"""

from pathlib import Path
import tempfile
import logging
from flask import (
    Flask,
    request,
    redirect,
    render_template,
    session,
    url_for,
    jsonify,
    abort
)
from botocore.exceptions import BotoCoreError, ClientError
from werkzeug.exceptions import RequestEntityTooLarge
from uploader import upload_file_s3


logger = logging.getLogger(__name__)


app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_A_SECURE_KEY'

VALID_USERS = {
    'admin': '1234',  # логин: пароль
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login web page logic"""
    if request.method == 'POST':
        user_login = request.form.get('login')
        user_password = request.form.get('password')
        if (user_login in VALID_USERS) and (
             VALID_USERS[user_login] == user_password):
            session['user'] = user_login
            return redirect(url_for('index'))
        return render_template('login.html', error='Неверный логин или пароль')
    return render_template('login.html')


@app.route('/')
def index():
    """Main uploading web page logic"""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Upload to the s3 logic"""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    files = request.files.getlist('files')
    if not files:
        return jsonify({'success': False, 'message': 'No files received'}), 400

    try:
        for file in files:
            rel_path = file.filename
            temp_path = Path(tempfile.gettempdir()) / rel_path
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            file.save(temp_path)

            try:
                upload_file_s3(temp_path, key=rel_path)
            except (BotoCoreError, ClientError) as s3_error:
                logger.error("S3 upload failed: %s", s3_error)
                return jsonify({'success': False,
                                'message': 'S3 upload failed'}), 500

    except RequestEntityTooLarge:
        return jsonify({'success': False, 'message': 'File too large'}), 413
    except OSError as fs_error:
        logger.exception("Filesystem error during temp file save: %s",
                         fs_error)
        return jsonify({'success': False, 'message': 'Filesystem error'}), 500

    return jsonify({'success': True})


@app.route('/logout')
def logout():
    """Logout logic for the user"""
    session.clear()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    """Not Found Error logic"""
    return render_template('error.html', code=404, message="Страница не найдена", link_text="На главную 🙏🏻"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """Not allowed error logic"""
    return render_template('error.html', code=405, message="Метод не поддерживается", link_text="Назад домой 🙏🏻"), 405


@app.errorhandler(500)
def server_error(e):
    """500 Error logic"""
    return render_template('error.html', code=500, message="Что-то пошло не так", link_text="Попробовать снова 🙏🏻"), 500


if __name__ == '__main__':
    app.run(debug=True)
