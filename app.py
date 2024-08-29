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
            avatar_url = user_data.get('avatar_url', " ")
            name = user_data.get('name', " ")
            login_name = user_data.get('login', "Error: Followers data not found")
            bio = user_data.get('bio', " ")
            create_date = user_data.get('created_at', " ")
            profile_chart =f"https://ghchart.rshah.org/0f786a/{username}"
            followers_count = user_data.get('followers', "Error: Followers data not found")
            following_count = user_data.get('following', "Error: Following data not found")
            gists_count = user_data.get('public_gists', "Error: Gists data not found")
            user_statistics = f"https://github-readme-stats.vercel.app/api?username={username}&theme=react&show_icons=true&hide_border=true&count_private=true"
            streaks =f"https://streak-stats.demolab.com?user={username}&theme=react&show_icons=true&hide_border=true&count_private=true"
            languages_used = f"https://github-readme-stats.vercel.app/api/top-langs/?username={username}&theme=react&show_icons=true&hide_border=true&layout=compact"
            # Fetch repository data
            repos_response = requests.get(f'https://api.github.com/users/{username}/repos')
            if repos_response.status_code == 200:
                repos_data = repos_response.json()
                repos_count = len(repos_data)


                session['avatar_url'] = avatar_url
                session['name'] = name
                session['login_name'] = login_name
                session['bio'] = bio
                session['create_date'] = create_date
                session['profile_chart'] = profile_chart
                session['repos_count'] = repos_count
                session['followers_count'] = followers_count
                session['following_count'] = following_count
                session['gists_count'] = gists_count
                session['user_statistics'] = user_statistics
                session['streaks'] = streaks
                session['languages_used'] = languages_used
            else:
                repos_count = "Error: Could not retrieve repositories data"
            print(user_statistics)
        else:
            followers_count = "Error: Could not retrieve user data"
    else:
        followers_count = following_count = gists_count = repos_count = " "
    
        session['avatar_url'] = avatar_url
        session['name'] = name
        session['repos_count'] = repos_count
        session['login_name'] = login_name
        session['bio'] = bio
        session['create_date'] = create_date
        session['profile_chart'] = profile_chart
        
        session['followers_count'] = followers_count
        session['following_count'] = following_count
        session['gists_count'] = gists_count
        session['user_statistics'] = user_statistics
        session['streaks'] = streaks
        session['languages_used'] = languages_used

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
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
