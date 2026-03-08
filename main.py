from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

@app.route('/check-password', methods=['POST'])
def check_password():
    from flask import request, jsonify
    data = request.get_json()
    if data.get('password') == ADMIN_PASSWORD:
        return jsonify({'correct': True})
    return jsonify({'correct': False})

if __name__ == '__main__':
    app.run()
