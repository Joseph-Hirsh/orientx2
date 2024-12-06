import json
import pandas as pd
from datetime import datetime
import re


def load_mp_dict(json_file):
    """Load and return the MP dictionary from a JSON file."""
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def parse_tweets(json_file, mp_dict_path, start_date=datetime(2013, 1, 1), end_date=datetime(2024, 3, 29)):
    """
    Parse tweets and match them with the poster's party from the MP dictionary.

    Args:
        json_file (str): Path to the JSON file containing tweet data.
        mp_dict_path (str): Path to the JSON file containing the MP dictionary.
        start_date (datetime): The starting date for filtering tweets (default is January 1, 2013).
        end_date (datetime): The ending date for filtering tweets (default is March 29, 2024).

    Returns:
        pd.DataFrame: A DataFrame containing parsed tweet data.
    """
    mp_dict = load_mp_dict(mp_dict_path)
    rows = []

    with open(json_file, 'r', encoding='utf-8') as file:
        unknowns = set()
        for line in file:
            tweet = parse_tweet(line, mp_dict, start_date, end_date)

            if tweet:
                if tweet.get("real name") == "Unknown":
                    unknowns.add((tweet.get("online name"), tweet.get("twitter handle")))

                rows.append(tweet)

        print(f"Unknown posters: {unknowns}")

    return pd.DataFrame(rows)


def parse_tweet(line, mp_dict, start_date, end_date):
    """Parse a single tweet and return its formatted data."""
    try:
        tweet = json.loads(line)
        tweet_date = _parse_date(tweet.get("created_at", ""))

        # Skip tweets outside the date range
        if tweet_date and (tweet_date < start_date or tweet_date > end_date):
            return None

        twitter_handle = f"@{tweet.get('user', {}).get('screen_name', '')}"
        poster_name = mp_dict.get(twitter_handle, {}).get("Name", "Unknown")

        if poster_name == "Unknown":
            return None

        party = mp_dict.get(twitter_handle, {}).get("Party", "Unknown")
        referendum_vote = mp_dict.get(twitter_handle, {}).get("Referendum vote", "Unknown")

        content = _strip_newlines(_replace_amp(get_tweet_text(tweet)))
        content = _remove_links(content)  # Remove links from the content
        content = _remove_handles(content)  # Remove any lingering Twitter handles

        return {
            "name": poster_name,
            "party": party,
            "content": content,
            "date": tweet_date,
            "retweets": tweet.get("retweet_count", 0),
            "favorites": tweet.get("favorite_count", 0),
            "referendum vote": referendum_vote
        }
    except json.JSONDecodeError:
        print("Error decoding JSON for a line. Skipping.")
        return None


def _remove_links(text):
    """Remove all links from the text."""
    # Regular expression to match URLs (http, https, ftp, etc.)
    return re.sub(r'http[s]?://\S+', '', text).strip()


def _remove_handles(text):
    """
    Remove "RT @twitterhandle:" and "@twitterhandle" from text.
    Args:
        text (str): The input text.
    Returns:
        str: Cleaned text with handles removed.
    """
    # Remove "RT @twitterhandle:" at the beginning
    text = re.sub(r'\bRT @\w+:\s*', '', text)
    # Remove all other "@twitterhandle"
    #text = re.sub(r'@\w+', '', text)
    # Strip extra spaces and return
    return text.strip()


def get_tweet_text(tweet):
    """Retrieve the text of a tweet, handling retweets and quote retweets."""
    if "retweeted_status" in tweet:  # Simple retweet
        original_tweet = tweet["retweeted_status"]
        original_author = original_tweet["user"]["screen_name"]
        original_text = original_tweet["text"]
        return _remove_handles(f"RT @{original_author}: {original_text}")
    elif "quoted_status" in tweet:  # Quote retweet
        user_text = tweet["text"]
        quoted_tweet = tweet["quoted_status"]
        quoted_author = quoted_tweet["user"]["screen_name"]
        quoted_text = quoted_tweet["text"]
        return _remove_handles(f"{user_text}\nQuoted: RT @{quoted_author}: {quoted_text}")
    else:  # Normal tweet
        return _remove_handles(tweet["text"])



def _parse_date(date_str):
    """Convert date string to datetime object."""
    try:
        return datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
    except ValueError:
        print(f"Error parsing date: {date_str}")
        return None


def _strip_newlines(text):
    """Remove newlines and extra spaces from text."""
    return text.replace("\n", " ").replace("\r", " ").strip()


def _replace_amp(text):
    """Replace '&amp;' with '&' in tweet text."""
    return text.replace("&amp;", "&")


def save_to_csv(df, output_csv_path):
    """Save DataFrame to CSV and print date range."""
    if not df.empty:
        print(f"Date range: {_get_date_range(df)}")

    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Data successfully saved to '{output_csv_path}'.")


def _get_date_range(df):
    """Return the date range of valid dates in the DataFrame."""
    valid_dates = df["date"].dropna()
    if not valid_dates.empty:
        return f"{valid_dates.min()} - {valid_dates.max()}"
    return "No valid dates found."

