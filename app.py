"""Main web site flask app module"""

from pathlib import Path
import tempfile
from flask import Flask, request, jsonify, render_template
from uploader import upload_file_s3

app = Flask(__name__)


@app.route('/')
def index():
    """Index page func"""
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    """Upload page func"""
    try:
        files = request.files.getlist('files')
        for file in files:
            rel_path = file.filename
            temp_path = Path(tempfile.gettempdir()) / rel_path
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            file.save(temp_path)
            upload_file_s3(temp_path, key=rel_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
