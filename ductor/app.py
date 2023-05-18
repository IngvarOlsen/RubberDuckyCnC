from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def settings():
    return render_template('settings.html')

@app.route('/save_settings', methods=['POST'])
def save_settings():
    settings = {
        'execute_script': False,
        'duck_file': ''
    }

    if 'execute_script' in request.form:
        settings['execute_script'] = True

    if 'duck_file' in request.form:
        settings['duck_file'] = request.form['duck_file']

    with open('settings.json', 'w') as file:
        json.dump(settings, file)

    return jsonify({'message': 'Settings saved successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)