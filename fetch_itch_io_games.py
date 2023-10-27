import os
import requests


def fetch_itch_io_games():
    key = os.environ['API_KEY']
    api = f'https://itch.io/api/1/{key}/my-games'

    response = requests.get(api)

    if response.status_code == 200:
        games_data = response.json()

        game_list = []
        for game in games_data["games"]:
            game_data = {
                "cover_url": game["cover_url"],
                "short_text": game["short_text"],
                "title": game["title"],
                "views_count": game["views_count"],
                "url": game["url"],
                "created_date": game["created_at"]  # Add the created_date parameter
            }
            game_list.append(game_data)

        # Sort the game_list based on the created_date
        game_list.sort(key=lambda x: x['created_date'], reverse=True)

        return game_list
    else:
        print("Request failed with status code", response.status_code)
        return None


def generate_game_markdown(game_list):
    markdown = "<div style='display: flex; flex-wrap: wrap; justify-content: left; font-family: Lato, sans-serif;'>\n"  # Added font
    for game_data in game_list:
        cover_url = game_data['cover_url']
        game_title = game_data['title']
        description = game_data['short_text']
        views_count = game_data['views_count']
        game_url = game_data['url']

        game_md = "<div style='width: 30%; text-align: left; margin-bottom: 20px; margin-right: 10px; margin-left: 10px;'>\n"
        game_md += f"<a href='{game_url}'><img src='{cover_url}' alt='{game_title}' style='width: 100%; border-radius: 12px; display: block; margin: 0 auto;' /></a>\n"
        game_md += f"<h4 style='margin-top: 5px; margin-bottom: 0px;'><a href='{game_url}' style='text-decoration: none; color: #dd4a4a;'>{game_title}</a></h4>\n"
        game_md += f"<p style='font-size: 12px; width: 100%; text-align: left; margin-bottom: 5px; margin-top: 5px'>{description}</p>\n"
        game_md += f"<div style='background-color: #3a3a3a; padding: 2.5px 5px; font-size: 8px; border-radius: 3px; margin-top: 3px; display: inline-block;'>Views: {views_count}</div>\n"  # Adjusted views style
        game_md += "</div>\n"

        markdown += game_md
    markdown += "</div>\n"

    return markdown


def write_readme(game_list):
    with open('README.md', 'r') as f:
        lines = f.readlines()

    new_lines = []
    replace_section = False

    for line in lines:
        if line.strip() == "<!--- BEGIN ITCH CARDS --->":
            replace_section = True
            new_lines.append(line)
            new_lines.append(generate_game_markdown(game_list))
        elif line.strip() == "<!--- END ITCH CARDS --->":
            replace_section = False
            new_lines.append(line)
        elif not replace_section:
            new_lines.append(line)

    with open('README.md', 'w') as f:
        f.writelines(new_lines)


write_readme(fetch_itch_io_games())