from flask import Flask, jsonify, request
from lab.scraper import Scraper

URL = 'http://apps.cs.utexas.edu/unixlabstatus/'

app = Flask(__name__)
scraper = Scraper(URL)

@app.route('/hosts/all', methods=['GET'])
def get_all_hosts():
    """List all UNIX hosts"""
    data = []
    for host in scraper.parse_html():
        host_vars = host.__dict__
        data.append(host_vars)
    return jsonify({
        'status': True,
        'data': data
    })

@app.route('/hosts/running', methods=['GET'])
def get_running_hosts():
    """List UNIX hosts whose status is up"""
    data = []
    for host in scraper.parse_html():
        host_vars = host.__dict__
        if host_vars['status']:
            name = host_vars['name']
            data.append(name)
    return jsonify({
        'status': True,
        'data': data
    })

@app.route('/hosts/<int:users>', methods=['GET'])
def get_hosts_with_users(users):
    """List UNIX hosts with users less than the threshold"""
    data = []
    for host in scraper.parse_html():
        host_vars = host.__dict__
        if host_vars['users'] < users:
            name = host_vars['name']
            data.append(name)
    return jsonify({
        'status': True,
        'data': data
    })

@app.route('/hosts/<float:load>', methods=['GET'])
def get_hosts_with_load(load):
    """List UNIX hosts with load less than the threshold"""
    data = []
    for host in scraper.parse_html():
        host_vars = host.__dict__
        if host_vars['load'] < load:
            name = host_vars['name']
            data.append(name)
    return jsonify({
        'status': True,
        'data': data
    })

#@app.route('/hosts/<str:name>', methods=['GET'])
#def get_specific_host(name):
#    pass

@app.route('/hosts/sorted', methods=['GET'])
def get_sorted_hosts(name):
    pass

if __name__ == '__main__':
    app.run(debug=True)
