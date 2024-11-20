import json
import pandas as pd
from datetime import datetime


def parse_tweets(json_file):
    rows = []

    with open(json_file, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet = json.loads(line)

                user = tweet.get("user", {})
                tweet_data = {
                    "poster name": user.get("name", ""),
                    "content": tweet.get("text", ""),
                    "date": _parse_date(tweet.get("created_at", "")),
                    "replies": tweet.get("reply_count", 0),
                    "reposts": tweet.get("retweet_count", 0),
                    "likes": tweet.get("favorite_count", 0),
                    "views": tweet.get("view_count", 0),
                }
                rows.append(tweet_data)
            except json.JSONDecodeError:
                print("Error decoding JSON for a line. Skipping.")
    return pd.DataFrame(rows)


def _parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
    except ValueError:
        print(f"Error parsing date: {date_str}")
        return None


def save_to_csv(df, output_csv_path):
    df.to_csv(output_csv_path, index=False)
    print(f"Data successfully saved to '{output_csv_path}'.")


