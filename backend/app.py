from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from file import sms_generator
import configparser

app = Flask(__name__)

# Autoriser les requêtes uniquement depuis http://localhost:3000
CORS(app, origins=["http://localhost:3000", "http://backend:5000"])
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'configFile' not in request.files:
        return jsonify({'error': 'No config file uploaded'}), 400

    config_file = request.files['configFile']
    config_file_path = os.path.join(app.config['UPLOAD_FOLDER'], config_file.filename)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    config_file.save(config_file_path)
    
    config = configparser.ConfigParser()
    config.read(config_file_path)
    
    ip = config.get('config', 'ip')
    port = config.get('config', 'port')
    user = config.get('config', 'username')
    password = config.get('config', 'password')
    files = [config.get('config', 'files')]
    repeat = config.getboolean('config', 'repeat')
    amount = config.getint('config', 'Total')
    amount_per_sec = config.getint('config', 'SMS/sec')
    
    sms_gen = sms_generator(ip, port, user, password, files, repeat, amount, amount_per_sec)
    sms_gen.main(ip, port, user, password, files, repeat, amount_per_sec, amount, 1)
    
    return jsonify({'message': 'SMS generation started.'})

@app.route('/api/data', methods=['GET'])
def get_data():
    sms_gen = sms_generator()
    data = sms_gen.get_all_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

