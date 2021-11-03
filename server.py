from flask import Flask, request, render_template, jsonify
import time, json, os

DB_PATH = 'db.json'

if not os.path.exists(DB_PATH):
    with open(DB_PATH, 'w') as f:
        json.dump({}, f)

app = Flask(__name__)

@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)

@app.route('/browse')
def browse():
    with open(DB_PATH, 'r') as f:
        db = json.load(f)

    return render_template('browse.html', db=db)

@app.route('/register', methods=['POST'])
def register():
    client_code = str(request.form['code']).lower()
    client_ip_addr = request.form['ip_addr']
    client_port = request.form['port']
    updated_at = time.time()

    with open(DB_PATH, 'r') as f:
        db = json.load(f)

    if client_ip_addr not in db:
        db[client_ip_addr] = {
            'code': client_code,
            'ip_addr': client_ip_addr,
            'port': client_port,
        }

    db[client_ip_addr]['updated_at'] = updated_at

    with open(DB_PATH, 'w') as f:
        json.dump(db, f)

    return jsonify({
        'result': True,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32456, debug=False)
