from flask import session
import requests
from datetime import datetime

def display(username):
    if username:
        # Generate URLs for GitHub stats, streaks, and top languages using external services
        user_statistics = f"https://github-readme-stats.vercel.app/api?username={username}&theme=react&show_icons=true&hide_border=true&count_private=true"
        streaks = f"https://streak-stats.demolab.com?user={username}&theme=react&show_icons=true&hide_border=true&count_private=true"
        languages_used = f"https://github-readme-stats.vercel.app/api/top-langs/?username={username}&theme=react&show_icons=true&hide_border=true&layout=compact"
        
        # Store the stats URLs in the session for later retrieval
        session['user_statistics'] = user_statistics
        session['streaks'] = streaks
        session['languages_used'] = languages_used

        # Fetch GitHub user data from the GitHub API
        user_response = requests.get(f'https://api.github.com/users/{username}')
        if user_response.status_code == 200:
            user_data = user_response.json()

            # Extract key user data from the API response
            avatar_url = user_data.get('avatar_url', " ")
            name = user_data.get('name', " ")
            login_name = user_data.get('login', "Error: Followers data not found")
            bio = user_data.get('bio', " ")
            profile_chart = f"https://ghchart.rshah.org/0f786a/{username}"  # GitHub contribution chart
            followers_count = user_data.get('followers', "Error: Followers data not found")
            following_count = user_data.get('following', "Error: Following data not found")
            gists_count = user_data.get('public_gists', "Error: Gists data not found")
            created_date = user_data.get('created_at', " ")

            # Parse and format the account creation date
            date_str = created_date.rstrip('Z')  # Remove trailing 'Z' from the date string
            custom_format = datetime.fromisoformat(date_str)  # Convert ISO format to datetime
            create_date = custom_format.strftime('%d/%m/%Y %H:%M')  # Format to readable date

            # Fetch the repository data for the user
            repos_response = requests.get(f'https://api.github.com/users/{username}/repos')
            if repos_response.status_code == 200:
                repos_data = repos_response.json()
                repos_count = len(repos_data)  # Count the number of repositories
                
                # Store all relevant data in session variables
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
                # Handle error in case the repository data can't be retrieved
                repos_count = "Error: Could not retrieve repositories data"
        else:
            # In case of an error retrieving user data, set default values in the session
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
        # Clear all session data if no username is provided
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
