from flask import session
import requests
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
