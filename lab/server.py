from flask import Flask, jsonify, request
from lab.scraper import Scraper

URL = 'http://apps.cs.utexas.edu/unixlabstatus/'

app = Flask(__name__)
scraper = Scraper(URL)

@app.route('/all', methods=['GET'])
def get_all_hosts():
    data = []
    scraper.update()
    timestamp = scraper.get_timestamp()
    for host in scraper.get_hosts():
        host_vars = host.__dict__
        data.append(host_vars)
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

@app.route('/up', methods=['GET'])
def get_up_hosts():
    data = []
    scraper.update()
    timestamp = scraper.get_timestamp()
    for host in scraper.get_hosts():
        host_vars = host.__dict__
        if host_vars['status']:
            data.append(host_vars)
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

@app.route('/down', methods=['GET'])
def get_down_hosts():
    data = []
    scraper.update()
    timestamp = scraper.get_timestamp()
    for host in scraper.get_hosts():
        host_vars = host.__dict__
        if not host_vars['status']:
            data.append(host_vars)
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

@app.route('/users', methods=['GET'])
def get_hosts_by_users():
    data = []
    req = request.args
    up, threshold = bool(req['up']), int(req['threshold'])
    scraper.update()
    timestamp = scraper.get_timestamp()
    for host in scraper.get_hosts():
        host_vars = host.__dict__
        if up and host_vars['users'] <= threshold or \
        not up and host_vars['users'] >= threshold:
            data.append(host_vars)
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

@app.route('/load', methods=['GET'])
def get_hosts_by_load():
    data = []
    req = request.args
    up, threshold = bool(req['up']), float(req['threshold'])
    scraper.update()
    timestamp = scraper.get_timestamp()
    for host in scraper.get_hosts():
        host_vars = host.__dict__
        if up and host_vars['load'] <= threshold or \
        not up and host_vars['load'] >= threshold:
            data.append(host_vars)
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

@app.route('/uptime', methods=['GET'])
def get_hosts_by_uptime():
    data = []
    req = request.args
    up, threshold = bool(req['up']), int(req['threshold'])
    scraper.update()
    timestamp = scraper.get_timestamp()
    for host in scraper.get_hosts():
        host_vars = host.__dict__
        if up and host_vars['uptime'] <= threshold or \
        not up and host_vars['uptime'] >= threshold:
            data.append(host_vars)
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

@app.route('/host', methods=['GET'])
def get_host_by_name():
    data = []
    req = request.args
    name = req['name']
    scraper.update()
    timestamp = scraper.get_timestamp()
    for host in scraper.get_hosts():
        host_vars = host.__dict__
        if name == host_vars['name']:
            data.append(host_vars)
            break
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

@app.route('/sorted', methods=['GET'])
def get_sorted_hosts():
    scraper.update()
    timestamp = scraper.get_timestamp()
    hosts = sorted(scraper.get_hosts(),
        key=lambda x: (x.status, x.users, x.load)
    )
    data = [host.__dict__ for host in hosts]
    return jsonify({
        'status': True,
        'timestamp': timestamp,
        'data': data
    })

if __name__ == '__main__':
    app.run(debug=True)
