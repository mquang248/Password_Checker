from flask import Flask, render_template, request, jsonify
from password_checker import check_password_strength
from password_cracker import simulate_cracking
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.json.get('password')
    if not password:
        return jsonify({'error': 'No password provided'}), 400
    
    # Get password strength analysis
    strength_results = check_password_strength(password)
    
    # Simulate cracking (if password is weak)
    if strength_results['score'] < 3:
        cracking_simulation = simulate_cracking(password)
        strength_results['cracking_simulation'] = cracking_simulation
    
    return jsonify(strength_results)

if __name__ == '__main__':
    app.run(debug=False) 