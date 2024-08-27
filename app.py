import os
from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
import requests
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key_if_missing')

DEFAULT_NAME = "sindresorhus"
def display(username):
    if username:
        # Fetch user data
        user_response = requests.get(f'https://api.github.com/users/{username}')
        if user_response.status_code == 200:
            user_data = user_response.json()
            followers_count = user_data.get('followers', "Error: Followers data not found")
            following_count = user_data.get('following', "Error: Following data not found")
            gists_count = user_data.get('public_gists', "Error: Gists data not found")
            
            # Fetch repository data
            repos_response = requests.get(f'https://api.github.com/users/{username}/repos')
            if repos_response.status_code == 200:
                repos_data = repos_response.json()
                repos_count = len(repos_data)
            else:
                repos_count = "Error: Could not retrieve repositories data"
        else:
            followers_count = "Error: Could not retrieve user data"
    else:
        followers_count = following_count = gists_count = repos_count = " "
    
    session['repos_count'] = repos_count
    session['followers_count'] = followers_count
    session['following_count'] = following_count
    session['gists_count'] = gists_count

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        display(username)
            # Redirect to avoid form resubmission
        # return redirect(url_for('home'))
    else:
        # Default username
        username = DEFAULT_NAME
        display(username)
    # Retrieve data from session
    repos_count = session.get('repos_count', "N/A")
    followers_count = session.get('followers_count', "N/A")
    following_count = session.get('following_count', "N/A")
    gists_count = session.get('gists_count', "N/A")

    return render_template('home.html', followers_count=followers_count, repos_count=repos_count, following_count=following_count, gists_count=gists_count)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
