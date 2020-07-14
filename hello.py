#!/usr/bin/env python

from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
#    return '<h1>Hello is {}</h1>'.format(name)

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


if __name__ == '__main__':
    app.run(debug=True)
