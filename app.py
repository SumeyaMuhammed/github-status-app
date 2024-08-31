import os
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
import requests
from forms import RegistrationForm, LoginForm
from stats import display

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key_if_missing')

DEFAULT_NAME = "sindresorhus"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        session['username'] = username
        display(username)
        return redirect(url_for('home'))
    username = session.get('username', DEFAULT_NAME)

    if session.get('username') is None:
        username = DEFAULT_NAME
        display(username)

    # Retrieve data from session
    name = session.get('name', "N/A")
    repos_count = session.get('repos_count', "N/A")
    avatar_url = session.get('avatar_url', "N/A")
    login_name = session.get('login_name', "N/A")
    bio = session.get('bio', "N/A")
    create_date = session.get('create_date', "N/A")
    profile_chart = session.get('profile_chart', "N/A")
    
    followers_count = session.get('followers_count', "N/A")
    following_count = session.get('following_count', "N/A")
    gists_count = session.get('gists_count', "N/A")
    user_statistics = session.get('user_statistics', "N/A")
    streaks = session.get('streaks', "N/A")
    languages_used = session.get('languages_used', "N/A")

    return render_template('home.html',username=username,avatar_url=avatar_url, name=name, login_name=login_name, bio=bio, create_date=create_date, profile_chart=profile_chart,
    followers_count=followers_count, repos_count=repos_count, following_count=following_count, gists_count=gists_count,user_statistics=user_statistics, streaks=streaks, languages_used=languages_used)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Log In', form=form)


if __name__ == '__main__':
    app.run(debug=True)
