import sys
import time
from pathlib import Path

from orientx2.parser import parse_tweets, save_to_csv


def main():
    current_dir = Path(__file__).resolve().parent
    json_file_path = current_dir.parent.parent / 'assets' / 'MPs.tweets.json'
    output_csv_path = current_dir.parent.parent / 'assets' / 'parsed_posts.csv'
    mp_dict_path = current_dir.parent.parent / 'assets' / 'uk_mps.json'

    start_time = time.time()

    df = None

    try:
        df = parse_tweets(json_file_path, mp_dict_path)
        print(df)

    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        print(f"\nProcess interrupted after {elapsed_time:.2f} seconds.")
        sys.exit(0)

    finally:
        try:
            save_to_csv(df, output_csv_path)
        except Exception as e:
            print(f"Error saving to CSV: {e}")

        elapsed_time = time.time() - start_time
        print(f"Process completed in {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    main()
