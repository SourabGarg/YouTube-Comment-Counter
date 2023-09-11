import requests

url = "https://youtu.be/AkyMZGnjm7c?si=sinZpV1814r81Hn_"
video_id = "v0RWnNj6f8c"

api_key = "Your API key"
min_comment_count = int(input("Please specify the minimum number of comments to search for:"))
print("Loading...")


def fetch_comments(api_key, video_id, page_token=None):
    try:
        URL = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&videoId={video_id}&part=snippet&maxResults=100'
        if page_token:
            URL += f'&pageToken={page_token}'

        response = requests.get(URL)
        response_data = response.json()
        user_comment_count = {}

        for item in response_data.get('items', []):
            snippet = item['snippet']['topLevelComment']['snippet']
            author_display_name = snippet['authorDisplayName']
            author_id = snippet['authorChannelId']['value']  # Get user ID
            if author_display_name in user_comment_count:
                user_comment_count[author_display_name]['count'] += 1
            else:
                user_comment_count[author_display_name] = {
                    'count': 1,
                    'id': author_id
                }

        next_page_token = response_data.get('nextPageToken')
        return user_comment_count, next_page_token

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}, None


def get_users_with_more_than_min_comments(api_key, video_id, min_count):
    try:
        user_comment_count = {}
        page_token = None

        while True:
            response_data, page_token = fetch_comments(api_key, video_id, page_token)

            for user, info in response_data.items():
                if user in user_comment_count:
                    user_comment_count[user]['count'] += info['count']
                else:
                    user_comment_count[user] = info

            if not page_token:
                break
        users_with_more_than_min_comments = [
            {'user_id': info['id'], 'username': user, 'comment_count': info['count']}
            for user, info in user_comment_count.items() if info['count'] > min_count
        ]

        return users_with_more_than_min_comments

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':
    users_with_more_than_min_comments = get_users_with_more_than_min_comments(api_key, video_id, min_comment_count)

    if users_with_more_than_min_comments is not None:
        print(f"Users who commented more than {min_comment_count} times on the video:")
        for user_info in users_with_more_than_min_comments:
            print(f"User ID: {user_info['user_id']}, Username: {user_info['username']}, Comment Count: {user_info['comment_count']}")
        print("Done!")
    else:
        print("No results were found.")
