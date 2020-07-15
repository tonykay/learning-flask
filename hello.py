#!/usr/bin/env python

from flask import Flask, redirect, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

site_title = 'N-Tier App'
site = { 'title' : "N Tier Flask App" }

@app.route('/')
def index():
    return render_template('index.html', site=site)

@app.route('/user/<name>')
def user(name):
    # return render_template('user.html', name=name, site_title=site_title)
    return render_template('user.html', name=name, site_title=site_title, site=site)
#    return '<h1>Hello is {}</h1>'.format(name)

@app.route('/user2/<name>')
def user2(name):
    return render_template('user2.html', name=name, site_title=site_title, site=site)

@app.route('/user/<int:id>')
def id(id):
    id = id * id
    return '<h1>Hello is {}</h1>'.format(id)

@app.route('/redirect')
def redirect_site():
    return redirect('http://google.com')

@app.route('/requests')
def request():
    user_agent = app.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', site=site), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', site=site), 500
if __name__ == '__main__':
    app.run(debug=True)
