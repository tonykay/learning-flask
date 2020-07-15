#!/usr/bin/env python

from flask import Flask, redirect, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'r3dh4t1!'   # For now, externalize later

bootstrap = Bootstrap(app)

site = { 'title' : "N Tier Flask App" }

@app.route('/')
def index():
    return render_template('index.html', site=site)

@app.route('/pip')                      # Playing with existing blog page - iFrames better?
def cheat_pip():
    return render_template('pip.html', site=site)

@app.route('/iframe')                   # Playing with iFrames
def iframe():
    return render_template('try_iframe.html', site=site)

@app.route('/user/<name>')              # Simple dynamic content
def user(name):
    return render_template('user.html', name=name, site=site)
    # return render_template('user.html', name=name, site_title=site_title)
    # return '<h1>Hello is {}</h1>'.format(name)

@app.route('/user2/<name>')
def user2(name):
    return render_template('user2.html', name=name, site=site)

@app.route('/user/<int:id>')            # learning, simple add view function by dynamic type
def id(id):
    id = id * id
    return '<h1>Hello is {}</h1>'.format(id)

@app.route('/redirect')                 # Simple redirect
def redirect_site():
    return redirect('http://google.com')

@app.route('/requests')                 # TODO: Not returning headers "AttributeError: 'Flask' object has no attribute 'headers'"
def request():
    user_agent = app.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

@app.errorhandler(404)                  # Simple 404 Error handler
def page_not_found(e):
    return render_template('404.html', site=site), 404

@app.errorhandler(500)                  # Simple 500 Server error
def internal_server_error(e):
    return render_template('500.html', site=site), 500
if __name__ == '__main__':
    app.run(debug=True)
