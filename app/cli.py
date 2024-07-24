from argparse import ArgumentParser
from datetime import datetime
from facebook_scraper import get_posts
import json
import requests
import os

def download_media(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading media: {e}")

def scrape_public_videos(profile_id, since, until):
    posts = []
    media_dir = 'downloaded_videos'
    os.makedirs(media_dir, exist_ok=True)
    
    for post in get_posts(profile_id, pages=10, options={"posts_per_page": 50}):
        post_date = post['time']
        if since <= post_date <= until and post['post_type'] == 'video':
            video_url = post['video']
            if video_url:
                video_filename = f"{media_dir}/{post['post_id']}.mp4"
                download_media(video_url, video_filename)
                post['video_local_path'] = video_filename
            posts.append(post)
    return posts

def main():
    parser = ArgumentParser(prog='cli')

    parser.add_argument('--start-date', type=str, required=True, help='Start date for scraping (format: YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, required=True, help='End date for scraping (format: YYYY-MM-DD)')
    parser.add_argument('--profile-id', type=str, required=True, help='The Facebook profile ID or username to scrape')

    args = parser.parse_args()

    # Validate date format
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
        return

    # Print arguments (for testing purposes)
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Profile ID: {args.profile_id}")

    # Scrape public videos
    public_videos = scrape_public_videos(args.profile_id, start_date, end_date)

    # Save the data to a JSON file
    with open('public_videos.json', 'w') as f:
        json.dump(public_videos, f, indent=4)

    print("Data scraping completed. Check public_videos.json for results and downloaded_videos directory for media files.")

if __name__ == '__main__':
    main()
