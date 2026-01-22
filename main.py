import os

from datetime import datetime
from loguru import logger

from app.github_app import GitHubAnalytics

from tasks.analise_dados import (
    get_lenguages_used,
    get_weekly_activity,
    create_visualizations,
    generate_linkedin_post,
    save_data
)

def main():

    os.makedirs("data", exist_ok=True)
    os.makedirs('charts', exist_ok=True)

    github_app = GitHubAnalytics()

    repos = github_app.get_user_repos()
    languages = get_lenguages_used(repos=repos)

    events = github_app.get_user_events()
    activity_data = get_weekly_activity(events=events)
    activity_data["repos"] = repos

    stats = github_app.get_repo_stats()

    create_visualizations(data=activity_data, languages=languages)

    post_content = generate_linkedin_post(data=activity_data, languages=languages)

    languages = languages if languages else None

    save_data({
        'languages': languages,
        'activity': activity_data,
        'generated_at': str(datetime.now().isoformat()),
        'post_content': post_content
    })

    with open('linkedin_post.txt', 'w', encoding='utf-8') as f:
        f.write(post_content)


    logger.info("")

if __name__ == "__main__":
    main()