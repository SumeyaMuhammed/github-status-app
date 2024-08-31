from flask import session
import requests
def display(username):
    if username:

        user_statistics = f"https://github-readme-stats.vercel.app/api?username={username}&theme=react&show_icons=true&hide_border=true&count_private=true"
        streaks =f"https://streak-stats.demolab.com?user={username}&theme=react&show_icons=true&hide_border=true&count_private=true"
        languages_used = f"https://github-readme-stats.vercel.app/api/top-langs/?username={username}&theme=react&show_icons=true&hide_border=true&layout=compact"
        session['user_statistics'] = user_statistics
        session['streaks'] = streaks
        session['languages_used'] = languages_used

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
        else:
            session['avatar_url'] = "N/A"
            session['name'] = "N/A"
            session['login_name'] = "N/A"
            session['bio'] = "N/A"
            session['create_date'] = "N/A"
            session['profile_chart'] = "N/A"
            session['repos_count'] = "N/A"
            session['followers_count'] = "N/A"
            session['following_count'] = "N/A"
            session['gists_count'] = "N/A"

        
    else:
        # Clear session data if no username is provided
        session['avatar_url'] = "N/A"
        session['name'] = "N/A"
        session['login_name'] = "N/A"
        session['bio'] = "N/A"
        session['create_date'] = "N/A"
        session['profile_chart'] = "N/A"
        session['repos_count'] = "N/A"
        session['followers_count'] = "N/A"
        session['following_count'] = "N/A"
        session['gists_count'] = "N/A"
