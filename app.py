from flask import Flask, render_template, request, redirect, url_for, Response
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DONACIONS_FILE = os.path.join(BASE_DIR, 'donacions.json')
ADMIN_PASSWORD = 'admin123'  # Canvia-ho per seguretat real

def carregar_donacions():
    if os.path.exists(DONACIONS_FILE):
        with open(DONACIONS_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

def desar_donacions(donacions):
    with open(DONACIONS_FILE, 'w') as f:
        json.dump(donacions, f, indent=4)

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.password != ADMIN_PASSWORD:
            return Response('Accés no autoritzat.', 401, {'WWW-Authenticate': 'Basic realm="Login"'})
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    donacions = carregar_donacions()
    total = sum(d['quantitat'] for d in donacions)
    return render_template('index.html', donacions=donacions, total=total)

@app.route('/admin', methods=['GET', 'POST'])
@auth_required
def admin():
    if request.method == 'POST':
        nom = request.form.get('nom') or 'Anònim'
        quantitat = float(request.form.get('quantitat'))
        data = request.form.get('data') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        donacions = carregar_donacions()
        donacions.append({
            'nom': nom,
            'quantitat': quantitat,
            'data': data
        })
        desar_donacions(donacions)
        return redirect(url_for('admin'))

    donacions = carregar_donacions()
    return render_template('admin.html', donacions=donacions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
