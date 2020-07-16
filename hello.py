#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os

# setup for sqlite
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SECRET_KEY'] = 'r3dh4t1!'   # For now, externalize later
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
             'id': self.id,
              'name': self.username
        }


bootstrap = Bootstrap(app)              # Setting up bootstrap

site = { 'title' : "N Tier Flask App" } # My additions for Title, simplify passing metadata

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

class NameForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/api/v1/users')
def api_get_all():
    try:
        users = User.query.all()
        # return render_template('get_all.html', site=site)
        return  jsonify([e.serialize() for e in users])
    except Exception as e:
        return(str(e))    

@app.route('/api/v1/ping')
def api_ping():
    return jsonify('{ ping: "alive" }')

@app.route('/ping')
def ping():
    return "<h1>I'm alive</h1>"

@app.route('/get_users')
def get_all():
    try:
        users = User.query.all()
        return render_template('get_all.html', site=site, users=users)
    except Exception as e:
        return(str(e))    


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('form'))
    return render_template('first_form.html',
        site=site, form=form, name=session.get('name'),
        known=session.get('known', False))


@app.route('/')                         # Basic view function
def index():
    return render_template('index.html', site=site)

@app.route('/pip')                      # Playing with existing blog page - iFrames better?
def cheat_pip():
    return render_template('pip.html', site=site)

@app.route('/iframe')                   # Playing with iFrames
def iframe():
    return render_template('try_iframe.html', site=site)

@app.route('/docs')                   # Playing with iFrames
def ansible_docs():
    return render_template('ansible-docs.html', site=site)

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
